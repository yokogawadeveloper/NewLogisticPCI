from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions
from django.db.models import F
from .serializers import *
from .models import *
import pyodbc
import os


# ViewSets define the view behavior.

class ConnectionDispatchViewSet(viewsets.ModelViewSet):
    queryset = DispatchInstruction.objects.all()
    serializer_class = DispatchInstructionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get_db_connection(so_no):
        server = '10.29.15.180'
        database = 'Logisticks'
        username = 'sa'
        password = 'LogDB*$@#032024'
        connection = pyodbc.connect(
            f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
        connection_cursor = connection.cursor()
        # Execute query
        query = 'SELECT TOP 1 PONO, PODate, PaymentomText, PaymentomId, WarrantyPeriod,CustCode,SalePerson FROM WA_SaleOrderMaster WHERE SoNo = ?'
        connection_cursor.execute(query, so_no)
        result = connection_cursor.fetchone()
        if result:
            data = {
                'SONo': so_no,
                'PONO': result[0],
                'PODate': result[1],
                'PaymentText': result[2],
                'PaymentId': result[3],
                'WarrantyPeriod': result[4],
                'CustCode':result[5],
                'SalePerson':result[6]
            }
            return data

    @action(detail=False, methods=['post'], url_path='dump_dispatch_po_details')
    def dump_dispatch_po_details(self, request, pk=None):
        so_no = request.data.get('so_no')
        update_flag = request.data.get('update_flag')
        try:
            data = self.get_db_connection(so_no=so_no)
            cust_code = data['CustCode']
            if cust_code[0] == '0':
                cust_code = cust_code[1:]
            else:
                cust_code = data['CustCode']
            dispatch_op_details = DispatchPODetails.objects.filter(so_no=so_no)
            if update_flag:
                if dispatch_op_details.exists():
                    dispatch_op_details.delete()
                DispatchPODetails.objects.create(
                    so_no=data['SONo'],
                    po_no=data['PONO'],
                    po_date=data['PODate'],
                    payment_id=data['PaymentId'],
                    payment_text=data['PaymentText'],
                    sales_person=data['SalePerson'],
                    bill_to=cust_code,
                    created_by=request.user,
                    updated_by=request.user
                )
            else:
                if dispatch_op_details.exists():
                    serializer = DispatchPODetailSerializer(dispatch_op_details, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data, status=status.HTTP_302_FOUND)
            return Response({'msg': 'External Data successfully updated.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='dump_master_list')
    def dump_master_list(self, request, pk=None):
        so_no = request.data.get('so_no')
        dil_id = request.data.get('dil_id')
        try:
            server = '10.29.15.180'
            database = 'Logisticks'
            username = 'sa'
            password = 'LogDB*$@#032024'
            # Establish connection
            connection = pyodbc.connect( 'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            connection_cursor = connection.cursor()
            # Fetch item numbers based on so_no
            item_nos_query = MasterItemList.objects.filter(dil_id=dil_id).values_list('item_no', flat=True)
            item_nos = list(item_nos_query)
            # Construct SQL query with placeholders
            query = """WITH MaxSoIdCTE AS (SELECT MAX(SoId) AS MaxSoId FROM WA_SaleOrderMaster WHERE SoNo = ?) 
                        SELECT IT.*, IP.* 
                        FROM WA_ItemTable AS IT 
                        JOIN MaxSoIdCTE ON IT.SoId = MaxSoIdCTE.MaxSoId 
                        JOIN WA_ItemParameter AS IP ON IT.ItemId = IP.ItemId 
                        WHERE IT.ItemNo IN ({})
                    """.format(', '.join(['?'] * len(item_nos)))

            # Execute query with parameters
            params = [so_no] + item_nos
            connection_cursor.execute(query, params)
            results = connection_cursor.fetchall()
            json_results = [dict(zip([column[0] for column in connection_cursor.description], row)) for row in results]
            # return Response(json_results)
            for item in json_results:
                master_item = MasterItemList.objects.filter(item_no=item['ItemNo'], so_no=so_no, dil_id_id=dil_id)
                previous_serial_no_qty = master_item.first().serial_no_qty if master_item.exists() else 0
                master_item.update(
                    warranty_date=item['WarrantyDate'],
                    warranty_flag=True,
                    customer_po_sl_no=item['Customer PO Sl. No'],
                    customer_po_item_code=item['Customer Part No'],
                    serial_no_qty=previous_serial_no_qty + 1,
                    custom_po_flag=True
                )
                # Create & Delete new InlineItemList
                if (item['Serialnumber'] == '' or item['Serialnumber'] is None) and (item['TagNo'] == '' or item['TagNo'] is None):
                    pass
                else:
                    InlineItemList.objects.filter(master_item=master_item.first(),serial_no=item['Serialnumber'],tag_no=item['TagNo']).delete()
                    InlineItemList.objects.create(
                        master_item=master_item.first(),
                        serial_no=item['Serialnumber'],
                        tag_no=item['TagNo'],
                        component_no=item['ComponentNo'],
                        quantity=1,
                        scale_max=item['Scale-1Max'],
                        scale_min=item['Scale-1Min'],
                        scale_unit=item['Scale-1Unit'],
                        scale_output=item['Scale-1Ouptput'],
                        range_max=item['RangeMax'],
                        range_min=item['RangeMin'],
                        range_unit=item['RangeUnit'],
                        range_output=item['RangeOutput'],
                    )
            # update Master Item List
            master_lists = MasterItemList.objects.filter(dil_id=dil_id)
            master_serial_update = master_lists.filter(quantity=F('serial_no_qty'), serial_flag=False)
            master_serial_update.update(serial_flag=True)
            # Dispatch Update
            master_list_serial_flag_count = master_lists.filter(serial_flag=False).count()
            if master_list_serial_flag_count == 0:
                dispatch_instruction = DispatchInstruction.objects.get(dil_id=dil_id)
                dispatch_instruction.updated_serial_flag = True
                dispatch_instruction.save()
            connection.commit()
            connection_cursor.close()
            connection.close()
            return Response(json_results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
