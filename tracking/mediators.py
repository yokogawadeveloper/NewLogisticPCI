from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from .sources import *


class TruckTrackingViewSet(viewsets.ModelViewSet):
    queryset = TruckList.objects.all()
    serializer_class = TruckRequestSerializer

    def get_queryset(self):
        return TruckList.objects.filter(is_active=True)

    @action(methods=['post'], detail=False, url_path='get_truck_tracking_details')
    def get_truck_tracking_details(self, request, *args, **kwargs):
        try:
            data = request.data
            truck_req_id = self.get_queryset().filter(id=data['truck_id'])
            truck_req_id = truck_req_id.values('id')[0]['id']
            transportation_id = TruckRequest.objects.filter(id=truck_req_id)
            transportation_id = transportation_id.values('transporter_id')[0]['transporter_id']

            filter_data = TrackingTransportation.objects.filter(id=transportation_id, is_active=True)
            serializer = TrackingTransportationSerializer(filter_data, many=True, context={'request': request})
            serializer_data = serializer.data
            res = serializer_data[0]
            # return Response(res)
            # based on transportation name
            if res['transportation_name'] in "GATI KWE":
                pass
                # get_gati(data, res, request)

            elif res['transportation_name'] in "ARC":
                pass
                # get_arc(data, res, request)

            elif res['transportation_name'] in "SARASWATI LOGISTICS":
                pass
                # saraswati_logistic(data, res, request)

            elif res['transportation_name'] in "SAFEXPRESS":
                safe_express(data, res, request)

            elif res['transportation_name'] in "SAFEXPRESSSS":
                pass
                # safe_expresss(data, res, request)

            elif res['transportation_name'] in "TCI EXPRESS":
                tci_express(data, res, request)

            # after Updating the Delivery details
            filter_data = TruckDeliveryDetails.objects.filter(truck_list_id=data['truck_id'], is_active=True)
            serializer = TruckDeliveryDetailsSerializer(filter_data, many=True, context={'request': request})
            serializer_data = serializer.data
            # Update Employee Allocation
            loading_details = TruckLoadingDetails.objects.filter(truck_list_id=data['truck_id'])
            dil_id = loading_details.values('dil_id')[0]['dil_id']
            user_allocation = DAUserRequestAllocation.objects.filter(dil_id=dil_id, approve_status="Packing")
            approver_emp_id = user_allocation.values_list('emp_id_id', flat=True)

            if len(approver_emp_id) == 0:
                emp_id = []

            dil_filter = DispatchInstruction.objects.filter(dil_id=dil_id)
            arr = []
            dic = {
                "dil_id": dil_id,
                "so_no": dil_filter.values('so_no')[0]['so_no'],
                # "job_code": dil_filter.values('job_code')[0]['job_code'],
                # "jobcode_da_no": dil_filter.values('jobcode_da_no')[0]['jobcode_da_no'],
                "po_no": dil_filter.values('po_no')[0]['po_no'],
                "status": "Tracking Status",
                "tracking_person": User.objects.filter(id=request.user.id).values('name')[0]['name'],
                "email_to": arr,
                "current_location": "",
                "current_status": "",
                "module": "tracking_status"
            }
            # appending email to arr
            for obj in approver_emp_id:
                emp_id = User.objects.filter(id=obj).values('email')[0]['email']
                arr.append(emp_id)
            dic.update({"email_to": arr})
            return Response({'data':serializer_data,'response':dic})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
