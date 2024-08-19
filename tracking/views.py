from rest_framework import permissions, viewsets, status
from decimal import Decimal
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models import Max
from rest_framework.decorators import action
from django.db import transaction
from dispatch.serializers import *
from packing.serializers import *
from .serializers import *
import pandas as pd
import datetime
import random
import os


# Create your views here.
class SAPInvoiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = SAPInvoiceDetails.objects.all()
    serializer_class = SAPInvoiceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def convert_price_to_decimal(price_str):
        # Remove spaces and commas, then convert to Decimal
        cleaned_price = price_str.replace(" ", "").replace(",", "")
        return Decimal(cleaned_price)

    @action(detail=False, methods=['POST'], url_path='excel_import_sap_invoice_details')
    def excel_import_sap_invoice_details(self, request, pk=None):
        try:
            with transaction.atomic():
                file = request.FILES.get('file')
                if file:
                    df = pd.read_excel(file)
                    df = df.where(pd.notnull(df), None)
                    # df['Tax Invoice Date'] = df['Tax Invoice Date'].fillna(df['Tax Invoice Date'].iloc[0])
                    # df['Billing Create Date'] = df['Billing Create Date'].fillna(df['Billing Create Date'].iloc[0])
                    df['Delivery quantity'] = df['Delivery quantity'].fillna(0).astype(int)
                    df['Tax Invoice Assessable Value'] = df['Tax Invoice Assessable Value'].fillna(0).astype(int)
                    df['Tax Invoice Total Tax Value'] = df['Tax Invoice Total Tax Value'].fillna(0).astype(int)
                    df['Tax Invoice Total Value'] = df['Tax Invoice Total Value'].fillna('0').astype(int)
                    df['Item Price (Sales)'] = df['Item Price (Sales)'].apply(self.convert_price_to_decimal)
                    df['DO Item Packed Quantity'] = df['DO Item Packed Quantity'].fillna('0').astype(int)
                    for index, row in df.iterrows():
                        SAPInvoiceDetails.objects.update_or_create(
                            reference_no=row['Reference Document'],
                            delivery=row['Delivery'],
                            delivery_item=row['Delivery Item'],
                            tax_invoice_no=row['Tax Invoice Number (ODN)'],
                            tax_invoice_date=row['Tax Invoice Date'],
                            reference_doc_item=row['Reference Document Item'],
                            billing_no=row['Billing Number'],
                            billing_created_date=row['Billing Create Date'],
                            hs_code=row['HS Code'],
                            hs_code_export=row['HS Code Export'],
                            delivery_qty=row['Delivery quantity'],
                            delivery_unit=row['Unit (Delivery)'],
                            tax_invoice_assessable_value=row['Tax Invoice Assessable Value'],
                            tax_invoice_total_tax_value=row['Tax Invoice Total Tax Value'],
                            tax_invoice_total_value=row['Tax Invoice Total Value'],
                            sales_item_price=row['Item Price (Sales)'],
                            packing_status=row['Packing status'],
                            do_item_packed_qty=row['DO Item Packed Quantity'],
                            packed_qty_unit=row['Packed Quantity unit'],
                            created_by=request.user,
                            updated_by=request.user,
                        )
                    return Response({'status': 'success', 'message': 'File uploaded successfully'})
                else:
                    transaction.rollback()
                    return Response({'status': 'error', 'message': 'No file found'})
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='sap_invoice_sum_of_amount')
    def sap_invoice_sum_of_amount(self, request, *args, **kwargs):
        try:
            truck_id = request.data['truck_id']
            dispatch_ids = TruckLoadingDetails.objects.filter(truck_list_id=truck_id).values_list('dil_id', flat=True)
            dispatch_ins = DispatchInstruction.objects.filter(dil_id__in=dispatch_ids)
            dispatch_serializer = DispatchUnRelatedSerializer(dispatch_ins, many=True)
            for dispatch in dispatch_serializer.data:
                sap_invoice_details = SAPInvoiceDetails.objects.filter(delivery=dispatch['dil_no'])
                tax_invoice_no = sap_invoice_details.values('tax_invoice_no', 'tax_invoice_date').annotate(
                    sum=Sum('tax_invoice_total_value'))
                sap_serializer = SAPInvoiceDetailsSerializer(sap_invoice_details, many=True)
                # dispatch['sap_invoice_details'] = sap_serializer.data
                dispatch['total_tax_invoice_no'] = tax_invoice_no
            return Response(dispatch_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TruckTypeViewSet(viewsets.ModelViewSet):
    queryset = TruckType.objects.all()
    serializer_class = TruckTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TruckType.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TrackingTransportationViewSet(viewsets.ModelViewSet):
    queryset = TrackingTransportation.objects.all()
    serializer_class = TrackingTransportationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TrackingTransportation.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TruckRequestViewSet(viewsets.ModelViewSet):
    queryset = TruckRequest.objects.all()
    serializer_class = TruckRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TruckRequest.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        # Loop through each TruckRequest instance and retrieve related TruckRequestTypesList instances
        for truck_request in serializer.data:
            instance = TruckRequest.objects.get(id=truck_request['id'])
            truck_request_types_list = instance.truckrequesttypeslist_set.all()
            truck_request_types_list_serializer = TruckRequestTypesListSerializer(truck_request_types_list, many=True)
            truck_request['truck_request_types_list'] = truck_request_types_list_serializer.data
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='dynamic_filter_truck_request')
    def dynamic_filter_truck_request(self, request):
        try:
            filter_data = request.data['data_filter']
            date_flag = request.data['date_flag']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            if date_flag:
                truck_request = TruckRequest.objects.filter(created_at__range=[date_from, date_to], **filter_data)
            else:
                truck_request = TruckRequest.objects.filter(**filter_data)
            serializer = TruckRequestSerializer(truck_request, many=True)
            for truck_request in serializer.data:
                instance = TruckRequest.objects.get(id=truck_request['id'])
                truck_request_types_list = instance.truckrequesttypeslist_set.all()
                truck_request_types_list_serializer = TruckRequestTypesListSerializer(truck_request_types_list,
                                                                                      many=True)
                truck_request['truck_request_types_list'] = truck_request_types_list_serializer.data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TruckListViewSet(viewsets.ModelViewSet):
    queryset = TruckList.objects.all()
    serializer_class = TruckListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TruckList.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            print("Validated Data:", serializer.validated_data)
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['put'], url_path=r'update_transportation/(?P<pk>[^/.]+)')
    def update_transportation(self, request, pk=None):
        try:
            truck_list = self.get_object()
        except TruckList.DoesNotExist:
            return Response({'error': 'TruckList not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TruckTransportationUpdateSerializer(truck_list, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='create_truck_list')
    def create_truck_list(self, request):
        try:
            with transaction.atomic():
                data = request.data
                truck_list = data.get('truck_list')
                dispatch_list = data.get('dispatch_list')
                freight_basis = data.get('freight_basis')
                mode_of_shipment = data.get('mode_of_shipment')
                delivery_terms = data.get('delivery_terms')
                oa_details = data.get('oa_details')
                # filter most relevant
                transportation = TrackingTransportation.objects.get(id=data.get('transporter'))
                # Create truck request
                truck_request = TruckRequest.objects.create(
                    transporter=transportation,
                    pincode=data.get('pincode'),
                    status=data.get('status'),
                    remarks=data.get('remarks'),
                    created_by=request.user,
                    updated_by=request.user
                )
                # Create Truck List
                for truck_data in truck_list:
                    quantity = truck_data.get('quantity')
                    truck_type = TruckType.objects.get(id=truck_data.get('truck_type'))
                    oa_details = truck_data.get('oa_details')
                    # Create truck request types list
                    truck_request_types_list = TruckRequestTypesList.objects.create(
                        truck_request=truck_request,
                        truck_type=truck_type,
                        truck_count=quantity,
                    )
                    for i in range(quantity):
                        truck_id = TruckList.objects.create(
                            truck_type=truck_type,
                            transportation=transportation,
                            truck_request=truck_request,
                            truck_request_types_list=truck_request_types_list,
                            oa_details=oa_details,
                            created_by=request.user,
                            updated_by=request.user
                        )
                        for dispatch_data in dispatch_list:
                            dil_id = dispatch_data.get('dil_id')
                            # update dispatch
                            dispatch = DispatchInstruction.objects.get(dil_id=dil_id)
                            dispatch.mode_of_shipment_id = mode_of_shipment
                            dispatch.delivery_terms_id = delivery_terms
                            dispatch.freight_basis_id = freight_basis
                            dispatch.save()
                            # create Truck DIl Map
                            TruckDilMappingDetails.objects.create(
                                dil_id_id=dil_id,
                                truck_list_id=truck_id
                            )

                # create DA AUth
                for dispatch in dispatch_list:
                    DAAuthThreads.objects.create(
                        dil_id_id=dispatch.get('dil_id'),
                        emp_id=request.user.id,
                        remarks='Truck Allocated',
                        status='Truck Allocated',
                        created_by_id=request.user.id
                    )
                return Response({'message': 'Truck list created successfully'}, status=status.HTTP_201_CREATED)
        except TrackingTransportation.DoesNotExist:
            return Response({'error': 'Transportation not found'}, status=status.HTTP_400_BAD_REQUEST)
        except State.DoesNotExist:
            return Response({'error': 'State not found'}, status=status.HTTP_400_BAD_REQUEST)
        except District.DoesNotExist:
            return Response({'error': 'District not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Taluk.DoesNotExist:
            return Response({'error': 'Taluk not found'}, status=status.HTTP_400_BAD_REQUEST)
        except TruckType.DoesNotExist:
            return Response({'error': 'Truck type not found'}, status=status.HTTP_400_BAD_REQUEST)
        except DispatchInstruction.DoesNotExist:
            return Response({'error': 'Dispatch instruction not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='update_truck_list')
    def update_truck_list(self, request):
        try:
            with transaction.atomic():
                data = request.data
                truck_request_id = data.get('id')
                transporter_id = data.get('transporter')
                state = State.objects.get(id=data.get('state'))
                district = District.objects.get(id=data.get('district'))
                taluk = Taluk.objects.get(id=data.get('taluk'))
                truck_list = data.get('truck_list')
                # Main Logic
                transportation = TrackingTransportation.objects.get(id=transporter_id)
                truck_request = TruckRequest.objects.get(id=truck_request_id)
                # delete existing TruckRequestTypesList, TruckList
                TruckRequestTypesList.objects.filter(truck_request=truck_request).delete()
                TruckList.objects.filter(truck_request=truck_request).delete()
                # update truck request
                truck_request.transporter = transportation
                truck_request.state = state
                truck_request.district = district
                truck_request.taluk = taluk
                truck_request.pincode = data.get('pincode')
                truck_request.status = data.get('status')
                truck_request.remarks = data.get('remarks')
                truck_request.updated_by = request.user
                truck_request.save()
                for truck_data in truck_list:
                    quantity = truck_data.get('quantity')
                    truck_type = TruckType.objects.get(id=truck_data.get('truck_type'))
                    # create truck request types list
                    truck_request_types_list = TruckRequestTypesList.objects.create(
                        truck_request=truck_request,
                        truck_type=truck_type,
                        truck_count=truck_data.get('quantity')
                    )
                    for i in range(quantity):
                        TruckList.objects.create(
                            truck_type=truck_type,
                            transportation=transportation,
                            truck_request=truck_request,
                            truck_request_types_list=truck_request_types_list,
                            created_by=request.user,
                            updated_by=request.user
                        )
                return Response({'message': 'Truck list updated successfully', 'status': status.HTTP_201_CREATED})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='dynamic_filter_truck_list')
    def dynamic_filter_truck_list(self, request):
        try:
            filter_data = request.data['data_filter']
            date_flag = request.data['date_flag']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            if date_flag:
                truck_list = TruckList.objects.filter(created_at__range=[date_from, date_to], **filter_data)
            else:
                truck_list = TruckList.objects.filter(**filter_data)

            serializer = TruckListSerializer(truck_list, many=True)
            for data in serializer.data:
                dispatch_ids = TruckLoadingDetails.objects.filter(truck_list_id=data['id']).values_list('dil_id',
                                                                                                        flat=True)
                dispatch = DispatchInstruction.objects.filter(dil_id__in=dispatch_ids).distinct()
                dispatch_serializer = DispatchInstructionSerializer(dispatch, many=True)

                delivery_challan = DeliveryChallan.objects.filter(truck_list=data['id'])
                delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan.first(), many=False)

                data['delivery_challan'] = delivery_challan_serializer.data
                data['dispatch'] = dispatch_serializer.data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='truck_list_on_dil')
    def truck_list_on_dil(self, request):
        try:
            data = request.data
            truck_list_ids = TruckLoadingDetails.objects.filter(dil_id=data['dil_id']).values_list('truck_list_id', )
            truck_list = TruckList.objects.filter(id__in=truck_list_ids)
            serializer = TruckListSerializer(truck_list, many=True)
            for data in serializer.data:
                delivery_challan = DeliveryChallan.objects.filter(truck_list=data['id'])
                delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan.first(), many=False)
                data['delivery_challan'] = delivery_challan_serializer.data

                truck_delivery_details = TruckDeliveryDetails.objects.filter(truck_list_id=data['id'])
                truck_delivery_details_serializer = TruckDeliveryDetailsSerializer(truck_delivery_details.first(),
                                                                                   many=True)

                data['truck_delivery_details'] = truck_delivery_details_serializer.data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='checkout_truck_list')
    def checkout_truck_list(self, request):
        try:
            data = request.data
            truck_list_id = data['truck_list_id']
            truck_list = TruckList.objects.filter(id=truck_list_id)
            if truck_list.exists():
                truck_list.update(
                    check_out=datetime.datetime.now(),
                    check_out_remarks=data['check_out_remarks'],
                    check_out_by=request.user
                )
                return Response({'message': 'Truck checked out successfully', 'status': status.HTTP_200_OK})
            else:
                return Response({'error': 'Truck list not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='dynamic_dil_or_truck_list')
    def dynamic_dil_or_truck_list(self, request):
        global truck_list
        try:
            dispatch_filter = request.data['dispatch_filter']
            truck_filter = request.data['truck_filter']
            date_flag = request.data['date_flag']
            date_type = request.data['date_type']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            if dispatch_filter and truck_filter:
                if date_flag:
                    if date_type == "submitted_date":
                        dispatch = DispatchInstruction.objects.filter(**dispatch_filter,
                                                                      submitted_date__range=[date_from, date_to])
                        loading = TruckLoadingDetails.objects.filter(
                            dil_id__in=dispatch.values_list('dil_id', flat=True))
                        truck_list = TruckList.objects.filter(id__in=loading.values_list('truck_list_id', flat=True),
                                                              **truck_filter)
                    else:
                        columns_search = date_type + '__range'
                        dispatch = DispatchInstruction.objects.filter(**dispatch_filter).values_list('dil_id',
                                                                                                     flat=True)
                        loading = TruckLoadingDetails.objects.filter(dil_id__in=dispatch).values_list('truck_list_id',
                                                                                                      flat=True)
                        truck_list = TruckList.objects.filter(id__in=loading, **truck_filter,
                                                              **{columns_search: [date_from, date_to]})
                else:
                    dispatch = DispatchInstruction.objects.filter(**dispatch_filter)
                    loading = TruckLoadingDetails.objects.filter(dil_id__in=dispatch.values_list('dil_id', flat=True))
                    truck_list = TruckList.objects.filter(id__in=loading.values_list('truck_list_id', flat=True),
                                                          **truck_filter)

                # getting truck list details based on dispatch filter and truck filter
                serializer = TruckListSerializer(truck_list, many=True)
                for data in serializer.data:
                    loading_details = TruckLoadingDetails.objects.filter(truck_list_id=data['id'])
                    loading_details_serializer = TruckLoadingDetailsSerializer(loading_details.first(), many=False)

                    delivery_challan = DeliveryChallan.objects.filter(truck_list=data['id'])
                    delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan.first(), many=False)

                    truck_delivery_details = TruckDeliveryDetails.objects.filter(truck_list_id=data['id'])
                    truck_delivery_details_serializer = TruckDeliveryDetailsSerializer(truck_delivery_details.first(),
                                                                                       many=True)

                    data['delivery_challan'] = delivery_challan_serializer.data
                    data['loading_details'] = loading_details_serializer.data
                    data['truck_delivery_details'] = truck_delivery_details_serializer.data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Dispatch filter or Truck filter is required'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TruckDIlMappingViewSet(viewsets.ModelViewSet):
    queryset = TruckLoadingDetails.objects.all()
    serializer_class = TruckDIlMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TruckLoadingDetails.objects.filter(is_active=True)

    @action(methods=['post'], detail=False, url_path='create_truck_mapping_on_dil')
    def create_truck_mapping_on_dil(self, request):
        try:
            dil_ids = request.data['dil_ids']
            truck_list_id = request.data['truck_list_id']
            truck_list = TruckList.objects.get(id=truck_list_id)
            for dil_id in dil_ids:
                dispatch = DispatchInstruction.objects.get(dil_id=dil_id)
                truck_mapping = TruckDilMappingDetails(truck_list_id=truck_list, dil_id=dispatch,
                                                       created_by=request.user)
                truck_mapping.save()
                return Response({'message': 'Truck Mapping Created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='truck_mapping_based_on_dil')
    def truck_mapping_based_on_dil(self, request):
        try:
            dil_id = request.data['dil_id']
            truck_mapping = TruckDilMappingDetails.objects.filter(dil_id=dil_id)
            truck_list = TruckList.objects.filter(id__in=truck_mapping.values_list('truck_list_id', flat=True))
            truck_serializer = TruckListSerializer(truck_list, many=True)
            return Response(truck_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TruckLoadingDetailsViewSet(viewsets.ModelViewSet):
    queryset = TruckLoadingDetails.objects.all()
    serializer_class = TruckLoadingDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TruckLoadingDetails.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='create_loading_details')
    def create_loading_details(self, request):
        try:
            data = request.data
            box_list = data['box_list']
            dil_id = data['dil_id']
            truck_list_id = data['truck_list_id']
            vehicle_no = data['vehicle_no']
            driver_name = data['driver_name']
            driver_no = data['driver_no']
            remarks = data['remarks']
            with transaction.atomic():
                if data['courier_flag'] is True:
                    transporter = TrackingTransportation.objects.get(id=data['transporter'])
                    truck_request = TruckRequest.objects.create(transporter=transporter, status='Loaded',
                                                                remarks=remarks)
                    truck_request_type = TruckRequestTypesList.objects.create(truck_request=truck_request,
                                                                              truck_type_id=4, truck_count=1)
                    truck_list = TruckList.objects.create(
                        truck_type_id=4,
                        transportation=transporter,
                        truck_request=truck_request,
                        truck_request_types_list=truck_request_type,
                        created_by=request.user, updated_by=request.user
                    )
                    truck_list_id = truck_list.id
                # Main Logic
                truck_list = TruckList.objects.filter(id=truck_list_id)
                dispatch = DispatchInstruction.objects.filter(dil_id=dil_id)
                if truck_list.exists():
                    truck_list.update(
                        vehicle_no=vehicle_no,
                        driver_name=driver_name,
                        driver_no=driver_no,
                        loading_remarks=remarks,
                        loaded_flag=True,
                        loaded_date=datetime.datetime.now(),
                        tracking_status=2,
                        status='Loaded',
                        no_of_boxes=len(box_list)
                    )
                    for box in box_list:
                        box_code = box['box_code']
                        truck_loading_details_obj = {
                            'dil_id': dispatch.first(),
                            'truck_list_id': truck_list.first(),
                            'box_code': box_code,
                            'created_by_id': request.user.id,
                            'updated_by_id': request.user.id
                        }
                        TruckLoadingDetails.objects.create(**truck_loading_details_obj)
                        box_details = BoxDetails.objects.filter(box_code=box_code)
                        if box_details.exists():
                            box_details.update(loaded_flag=True, loaded_date=datetime.datetime.now())
                        else:
                            return Response({'error': 'Box code not found'}, status=status.HTTP_400_BAD_REQUEST)
                    # Update truck list status & Dispatch status
                    dispatch = DispatchInstruction.objects.filter(dil_id=dil_id)
                    dispatch.filter(dil_status_no__in=[11, 12, 13]).update(
                        dil_status_no=14,
                        dil_status='Loaded',
                        loaded_flag=True,
                        loaded_date=datetime.datetime.now()
                    )
                else:
                    return Response({'error': 'Truck list not found'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'loading details created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='loading_details_on_truck_list_id')
    def loading_details_on_truck_list_id(self, request):
        try:
            data = request.data
            truck_list_id = data['truck_list_id']
            truck_list = TruckList.objects.filter(id=truck_list_id)
            if truck_list.exists():
                loading_details = TruckLoadingDetails.objects.filter(truck_list_id=truck_list_id)
                serializer = TruckLoadingDetailsSerializer(loading_details, many=True)
                for data in serializer.data:
                    box_details = BoxDetails.objects.filter(box_code=data['box_code'])
                    box_details_serializer = BoxDetailSerializer(box_details, many=True)
                    data['box_details'] = box_details_serializer.data

                    box_details_count = BoxDetails.objects.filter(parent_box=data['box_code']).count()
                    # count = box_details_count.values('parent_box').annotate(count=Count('parent_box'))
                    # data['box_count'] = count[0]['count']
                    data['box_count'] = box_details_count
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Truck list not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='remove_loading_details_on_truck_list')
    def remove_loading_details_on_truck_list(self, request):
        try:
            data = request.data
            dil_id = data['dil_id']
            box_code = data['box_code']
            truck_list_id = data['truck_list_id']

            # Create Loading Details
            truck_loading_details_obj = {
                'dil_id': dil_id,
                'truck_list_id': truck_list_id,
                'box_code': box_code
            }

            # Remove Truck Loading Details
            loading = TruckLoadingDetails.objects.filter(**truck_loading_details_obj)
            loading.delete()

            # Update Box Details
            box_details = BoxDetails.objects.filter(box_code=box_code)
            if box_details.exists():
                box_details.update(loaded_flag=False)

            # Update Truck List status & Dispatch status
            truck_list_in_loading = TruckLoadingDetails.objects.filter(truck_list_id=truck_list_id).exists()
            if not truck_list_in_loading:
                TruckList.objects.filter(id=truck_list_id).update(
                    loaded_flag=False,
                    tracking_status=1,
                    status='Not Loaded',
                    no_of_boxes=0
                )

            DispatchInstruction.objects.filter(dil_id=dil_id).update(
                dil_status_no=13,
                dil_status='Loading In Progress',
                loaded_flag=False,
            )

            return Response({'message': 'Deletion done successfully'}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({'error': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeliveryChallanViewSet(viewsets.ModelViewSet):
    queryset = DeliveryChallan.objects.all()
    serializer_class = DeliveryChallanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryChallan.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='create_delivery_challan')
    def create_delivery_challan(self, request, *args, **kwargs):
        try:
            data = request.data
            truck_list_id = data.get('truck_list')
            dc_invoice_details = data.get('dc_inv_details')
            truck_list = TruckList.objects.filter(id=truck_list_id)
            truck_loading_details = TruckLoadingDetails.objects.filter(truck_list_id=truck_list_id)
            no_of_boxes = truck_list.first().no_of_boxes if truck_list.exists() else 0

            if truck_list.exists():  # Check if truck_list exists
                delivery_challan = DeliveryChallan.objects.create(
                    truck_list=truck_list.first(),
                    e_way_bill_no=data.get('e_way_bill_no'),
                    lrn_no=data.get('lrn_no'),
                    lrn_date=data.get('lrn_date'),
                    remarks=data.get('remarks'),
                    description_of_goods=data.get('description_of_goods'),
                    mode_of_delivery=data.get('mode_of_delivery'),
                    freight_mode=data.get('freight_mode'),
                    destination=data.get('destination'),
                    kind_attended=data.get('kind_attended'),
                    consignee_remakes=data.get('consignee_remakes'),
                    no_of_boxes=no_of_boxes,
                    created_by=request.user,
                    updated_by=request.user
                )
                for dc_inv in dc_invoice_details:
                    bill_no = dc_inv.get('bill_no')
                    bill_date = dc_inv.get('bill_date')
                    if bill_no:
                        dispatch = DispatchInstruction.objects.filter(dil_id=dc_inv.get('dil_id'))
                        DCInvoiceDetails.objects.create(
                            delivery_challan=delivery_challan,
                            truck_list=truck_list.first(),
                            dil_id=dispatch.first() if dispatch.exists() else None,
                            bill_no=dc_inv.get('bill_no'),
                            bill_date=bill_date,  # Assign formatted date or None
                            bill_type=dc_inv.get('bill_type'),
                            bill_amount=dc_inv.get('bill_amount'),
                            created_by=request.user,
                            updated_by=request.user
                        )

                serializer = DeliveryChallanSerializer(delivery_challan)
                # Update truck list status & Dispatch status
                truck_list.update(status='DC Created', tracking_status=3)
                dil_ids = truck_loading_details.values_list('dil_id', flat=True).distinct()
                dispatch = DispatchInstruction.objects.filter(dil_id__in=dil_ids)
                dispatch.update(dil_status_no=15, dil_status='DC Created')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Truck list not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='update_delivery_challan')
    def update_delivery_challan(self, request, *args, **kwargs):
        try:
            data = request.data
            challan_id = data.get('id')
            truck_list_id = data.get('truck_list')
            dc_invoice_details = data.get('dc_inv_details')
            # Main Logic
            delivery_challan = DeliveryChallan.objects.filter(id=challan_id)
            truck_list = TruckList.objects.filter(id=truck_list_id)
            if delivery_challan.exists():
                delivery_challan.update(
                    truck_list=truck_list.first(),
                    e_way_bill_no=data.get('e_way_bill_no'),
                    lrn_no=data.get('lrn_no'),
                    lrn_date=data.get('lrn_date'),
                    remarks=data.get('remarks'),
                    no_of_boxes=truck_list.first().no_of_boxes,
                    updated_by=request.user
                )
                # Delete existing invoice details
                DCInvoiceDetails.objects.filter(delivery_challan=delivery_challan.first()).delete()
                for dc_inv in dc_invoice_details:
                    bill_no = dc_inv.get('bill_no')
                    bill_date = dc_inv.get('bill_date')
                    # if bill_date:
                    #     bill_date = datetime.datetime.strptime(bill_date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                    # else:
                    #     bill_date = None
                    DCInvoiceDetails.objects.create(
                        delivery_challan=delivery_challan.first(),
                        truck_list=truck_list.first(),
                        dil_id_id=dc_inv.get('dil_id'),
                        bill_no=bill_no,
                        bill_date=bill_date,
                        bill_type=dc_inv.get('bill_type'),
                        bill_amount=dc_inv.get('bill_amount'),
                        created_by=request.user,
                        updated_by=request.user
                    )
                serializer = DeliveryChallanSerializer(delivery_challan.first())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Truck list not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='dynamic_filter_delivery_challan')
    def dynamic_filter_delivery_challan(self, request):
        try:
            filter_data = request.data['data_filter']
            date_flag = request.data['date_flag']
            date_from = request.data['date_from']
            date_to = request.data['date_to']
            # if date flag is true then filter with date range
            if date_flag:
                delivery_challan = DeliveryChallan.objects.filter(
                    created_at__range=[date_from, date_to], **filter_data)
            else:
                delivery_challan = DeliveryChallan.objects.filter(**filter_data)
            serializer = DeliveryChallanSerializer(delivery_challan, many=True)
            # based on list dispatch details
            for data in serializer.data:
                truck_loading_details = TruckLoadingDetails.objects.filter(truck_list_id=data['truck_list'])
                truck_loading_details_serializer = TruckLoadingDetailsSerializer(truck_loading_details, many=True)
                data['loading_details'] = truck_loading_details_serializer.data
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DCInvoiceDetailsViewSet(viewsets.ModelViewSet):
    queryset = DCInvoiceDetails.objects.all()
    serializer_class = DCInvoiceDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)


class InvoiceChequeDetailsViewSet(viewsets.ModelViewSet):
    queryset = InvoiceChequeDetails.objects.all()
    serializer_class = InvoiceChequeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InvoiceChequeDetails.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='dynamic_filter_invoice_cheque_details')
    def dynamic_filter_invoice_cheque_details(self, request):
        try:
            data = request.data
            invoice_cheque_details = InvoiceChequeDetails.objects.filter(**data)
            serializer = InvoiceChequeDetailsSerializer(invoice_cheque_details, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EWBDetailsViewSet(viewsets.ModelViewSet):
    queryset = EWBDetails.objects.all()
    serializer_class = EWBDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EWBDetails.objects.filter(is_active=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'], url_path='excel_import_ewb_details')
    def excel_import_ewb_details(self, request, pk=None):
        try:
            with transaction.atomic():
                file = request.FILES.get('file')
                if file:
                    df = pd.read_excel(file)
                    df = df.where(pd.notnull(df), None)
                    df['No of Items'] = df['No of Items'].fillna(0).astype(int)
                    df['SGST Value'] = df['SGST Value'].fillna(0).astype(float)
                    df['CGST Value'] = df['CGST Value'].fillna(0).astype(float)
                    df['IGST Value'] = df['IGST Value'].fillna(0).astype(float)
                    df['CESS Value'] = df['CESS Value'].fillna(0).astype(int)
                    df['CESS Non.Advol Value'] = df['CESS Non.Advol Value'].fillna(0).astype(int)
                    df['Other Value'] = df['Other Value'].fillna('0').astype(int)
                    df['Total Invoice Value)'] = df['Total Invoice Value'].fillna('0').astype(float)
                    df['EWB Date'] = pd.to_datetime(df['EWB Date'], errors='coerce')
                    df['Valid Till Date'] = pd.to_datetime(df['Valid Till Date'], errors='coerce')
                    # Fill NaT values with the default date
                    df['Valid Till Date'] = df['Valid Till Date'].fillna(datetime.date.today())
                    for index, row in df.iterrows():
                        ewb_details = EWBDetails.objects.update_or_create(
                            ewb_no=row['EWB No'],
                            ewb_date=row['EWB Date'],
                            supply_type=row['Supply Type'],
                            doc_no=row['Doc.No'],
                            doc_date=row['Doc.Date'],
                            doc_type=row['Doc.Type'],
                            other_party_gstin=row['Other Party GSTIN'],
                            transporter_details=row['Transporter Details'],
                            from_gstin=row['From GSTIN'],
                            to_gstin=row['TO GSTIN'],
                            from_gstin_info=row['From GSTIN Info'],
                            to_gstin_info=row['TO GSTIN Info'],
                            status=row['status'],
                            no_of_items=row['No of Items'],
                            main_hsn_code=row['Main HSN Code'],
                            main_hsn_desc=row['Main HSN Desc'],
                            assessable_value=row['Assessable Value'],
                            sgst_value=row['SGST Value'],
                            cgst_value=row['CGST Value'],
                            igst_value=row['IGST Value'],
                            cess_value=row['CESS Value'],
                            cess_non_adv_value=row['CESS Non.Advol Value'],
                            other_value=row['Other Value'],
                            total_invoice_value=row['Total Invoice Value'],
                            valid_till_date=row['Valid Till Date'],
                            other_party_rejection_status=row['Other Party Rejection Status'],
                            inr=row['IRN'],
                            gen_mode=row['Gen.Mode'],
                            created_by=request.user,
                            updated_by=request.user,
                        )
                    return Response({'message': 'EWB Details created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    transaction.rollback()
                    return Response({'status': 'error', 'message': 'No file found'})
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='ewb_details_with_ewb_no')
    def ewb_details_with_ewb_no(self, request, *args, **kwargs):
        try:
            data = request.data
            ewb_details = EWBDetails.objects.filter(ewb_no=data['ewb_no'])
            serializer = EWBDetailsSerializer(ewb_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GatePassInfoViewSet(viewsets.ModelViewSet):
    queryset = GatePassInfo.objects.filter(is_active=True)
    serializer_class = GatePassInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='update_gate_info_for_checkout')
    def update_gate_info_for_checkout(self, request, *args, **kwargs):
        try:
            data = request.data
            if data:
                gate_info = GatePassInfo.objects.filter(id=data['id'], is_active=True)
                truck_info_ids = GatePassTruckDetails.objects.filter(gate_info=data['id']).values('truck_info')
                truck_lists = TruckList.objects.filter(id__in=truck_info_ids)
                gate_info.update(
                    checkout_date=datetime.date.today(),
                    checkout_remarks=data['checkout_remarks'],
                    status_no=3
                )
                GatePassAuthThreads.objects.create(
                    gate_pass_info_id=data['id'],
                    emp=request.user,
                    status='Checkout',
                    remarks=data['checkout_remarks']
                )
                truck_lists.update(status='Checkout', tracking_status=4)
                truck_lists_ids = truck_lists.values_list('id', flat=True)
                truck_dil_map = TruckDilMappingDetails.objects.filter(truck_list_id_id__in=truck_lists_ids)
                dil_ids = truck_dil_map.values_list('dil_id', flat=True)
                DispatchInstruction.objects.filter(dil_id__in=dil_ids).update(
                    dil_status_no=17,
                    dil_status='Checkout From YIL',
                )
                return Response({'message': 'Gate Checkout is updated!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='delete_gate_info_for_checkout')
    def delete_gate_info_for_checkout(self, request, *args, **kwargs):
        try:
            data = request.data
            if data:
                gate_info = GatePassInfo.objects.filter(id=data['id'], is_active=True)
                gate_info.update(is_active=False)
                return Response({'message': 'Gate Info is deleted!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GatePassTruckDetailsViewSet(viewsets.ModelViewSet):
    queryset = GatePassTruckDetails.objects.all()
    serializer_class = GatePassTruckDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='create_gate_pass_truck_details')
    def create_gate_pass_truck_details(self, request, *args, **kwargs):
        try:
            data = request.data
            truck_list = data['truck_list']
            users = User.objects.filter(gate_pass_approve_flag=True)

            with transaction.atomic():
                if data:
                    last_gate_pass = GatePassInfo.objects.aggregate(Max('gate_pass_no'))
                    new_gate_pass_no = (last_gate_pass['gate_pass_no__max'] or 0) + 1
                    gate_pass_info = GatePassInfo.objects.create(
                        driver_name=data['driver_name'],
                        transporter_name=data['transporter_name'],
                        checkin_date=datetime.date.today(),
                        gate_pass_no=new_gate_pass_no,
                        gate_pass_type=data['gate_pass_type'],
                        normal_remarks=data['normal_remarks'],
                        status_no=1,
                        create_by=request.user,
                    )
                    # Gate Pass Auth create
                    GatePassAuthThreads.objects.create(
                        gate_pass_info=gate_pass_info,
                        emp=request.user,
                        status='Created',
                        remarks='Gate Pass Created',
                    )
                    # create Gate Pass Approver
                    for user in users:
                        GatePassApproverDetails.objects.create(
                            gate_info=gate_pass_info,
                            emp=user,
                            approver_status='gate_pass_approver',
                            status='Pending',
                            create_by=request.user,
                        )
                    # create Truck List
                    for truck in truck_list:
                        truck_instance = TruckList.objects.get(id=truck['id'])  # Get the actual truck instance
                        truck_dil_map = TruckDilMappingDetails.objects.filter(truck_list_id=truck_instance.id)
                        dil_ids = truck_dil_map.values_list('dil_id', flat=True)
                        GatePassTruckDetails.objects.create(
                            gate_info=gate_pass_info,
                            truck_info=truck_instance,
                            create_by=request.user,
                        )
                        truck_instance.status = 'Gate Pass Created'
                        truck_instance.tracking_status = 4
                        truck_instance.save()
                        # Update DIL
                        DispatchInstruction.objects.filter(dil_id__in=dil_ids).update(
                            dil_status_no=16,
                            dil_status='Gate Pass Created',
                        )
                    return Response({'message': 'Gate Pass Truck Details Created!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.rollback()
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='dynamic_filter_gate_pass_truck_details')
    def dynamic_filter_gate_pass_truck_details(self, request, *args, **kwargs):
        try:
            data = request.data
            gate_pass_info = GatePassInfo.objects.filter(**data, is_active=True)
            gate_pass_info_serializer = GatePassInfoSerializer(gate_pass_info, many=True)
            for gate_pass_info_data in gate_pass_info_serializer.data:
                gate_pass_info_id = gate_pass_info_data['id']
                truck_ids = GatePassTruckDetails.objects.filter(gate_info=gate_pass_info_id).values_list('truck_info',
                                                                                                         flat=True)
                # Aggregate the sum of the number of boxes for the retrieved truck IDs
                sum_of_no_of_boxes = \
                    TruckList.objects.filter(id__in=truck_ids).aggregate(total_boxes=Sum('no_of_boxes'))['total_boxes']
                truck_data = TruckList.objects.filter(id__in=truck_ids)
                truck_serializer = TruckListSerializer(truck_data, many=True)
                truck_serializer_data = truck_serializer.data
                for truck_data in truck_serializer_data:
                    dispatch_ids = TruckLoadingDetails.objects.filter(truck_list_id=truck_data['id']).values_list(
                        'dil_id', flat=True)
                    dispatch = DispatchInstruction.objects.filter(dil_id__in=dispatch_ids).distinct()
                    dispatch_serializer = DispatchInstructionSerializer(dispatch, many=True)

                    delivery_challan = DeliveryChallan.objects.filter(truck_list=truck_data['id']).first()
                    delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan, many=False)

                    truck_data['delivery_challan'] = delivery_challan_serializer.data
                    truck_data['dispatch'] = dispatch_serializer.data
                gate_pass_info_data['truck_list'] = truck_serializer_data
                gate_pass_info_data['sum_of_no_of_boxes'] = sum_of_no_of_boxes
            serialized_data = gate_pass_info_serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GatePassApproverDetailsViewSet(viewsets.ModelViewSet):
    queryset = GatePassApproverDetails.objects.all()
    serializer_class = GatePassApproverDetailsSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['post'], detail=False, url_path='gate_pass_approver_details_by_user')
    def gate_pass_approver_details_by_user(self, request, *args, **kwargs):
        try:
            user = request.user
            gate_info_ids = GatePassApproverDetails.objects.filter(emp=user, approver_flag=False).values_list(
                'gate_info', flat=True)
            gate_pass_info = GatePassInfo.objects.filter(id__in=gate_info_ids, is_active=True)
            gate_pass_info_serializer = GatePassInfoSerializer(gate_pass_info, many=True)
            for gate_pass_info_data in gate_pass_info_serializer.data:
                gate_pass_info_id = gate_pass_info_data['id']
                truck_ids = GatePassTruckDetails.objects.filter(gate_info=gate_pass_info_id).values_list('truck_info',
                                                                                                         flat=True)
                # Aggregate the sum of the number of boxes for the retrieved truck IDs
                sum_of_no_of_boxes = \
                    TruckList.objects.filter(id__in=truck_ids).aggregate(total_boxes=Sum('no_of_boxes'))['total_boxes']

                truck_data = TruckList.objects.filter(id__in=truck_ids)
                truck_serializer = TruckListSerializer(truck_data, many=True)
                truck_serializer_data = truck_serializer.data
                for truck_data in truck_serializer_data:
                    dispatch_ids = TruckLoadingDetails.objects.filter(truck_list_id=truck_data['id']).values_list(
                        'dil_id', flat=True)
                    dispatch = DispatchInstruction.objects.filter(dil_id__in=dispatch_ids).distinct()
                    dispatch_serializer = DispatchInstructionSerializer(dispatch, many=True)

                    delivery_challan = DeliveryChallan.objects.filter(truck_list=truck_data['id']).first()
                    delivery_challan_serializer = DeliveryChallanSerializer(delivery_challan, many=False)

                    truck_data['delivery_challan'] = delivery_challan_serializer.data
                    truck_data['dispatch'] = dispatch_serializer.data
                gate_pass_info_data['truck_list'] = truck_serializer_data
                gate_pass_info_data['sum_of_no_of_boxes'] = sum_of_no_of_boxes
            serialized_data = gate_pass_info_serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='update_gate_pass_approver_details')
    def update_gate_pass_approver_details(self, request, *args, **kwargs):
        try:
            data = request.data
            gate_pass_id = data['gate_pass_id']
            remarks = data['remarks']
            gate_pass_info = GatePassInfo.objects.filter(id=gate_pass_id, is_active=True)
            gate_pass_info.update(status_no=2, approve_by=request.user, approved_date=timezone.now())
            gate_pass_approver = GatePassApproverDetails.objects.filter(gate_info=gate_pass_id)
            gate_pass_approver.update(
                approver_status="Gate Pass Approved",
                status_no=2,
                approver_flag=True,
                remarks=remarks
            )
            GatePassAuthThreads.objects.create(
                gate_pass_info_id=gate_pass_id,
                emp=request.user,
                status='Approved',
                remarks=remarks,
                created_by=request.user,
            )
            return Response({'message': 'Update Gate Approver Done!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
