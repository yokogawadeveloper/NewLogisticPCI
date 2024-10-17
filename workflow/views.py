from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from accounts.serializers import EmployeeUserSerializer
from .serializers import *
from django.db.models import Max


# Create your views here.
class WorkFLowTypeViewSet(viewsets.ModelViewSet):
    queryset = WorkFlowType.objects.all()
    serializer_class = WorkFlowTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True, context={'request': request})
        serializer_data = serializer.data
        return Response(serializer_data)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            request_data = {
                "wf_name": data['wf_name'],
                "slug_name": data['slug_name'],
                "total_level": data['flow_details'][-1]['level'],
            }
            serializer = WorkFlowTypeSerializer(data=request_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                # Create WorkFlowControl and WorkFlowEmployees objects
                for val in data['flow_details']:
                    WorkFlowControl.objects.create(
                        wf_id_id=serializer_data['wf_id'],
                        approver=val['approver'],
                        level=val['level'],
                        parallel=val['parallel'],
                        created_by_id=request.user.id
                    )
                    # Fetch latest wfc_id
                    wfc_id = WorkFlowControl.objects.values('wfc_id').latest('wfc_id')['wfc_id']
                    # Create WorkFlowEmployees objects
                    WorkFlowEmployees.objects.create(
                        wfc_id_id=wfc_id,
                        emp_id=val['emp_id'],
                        created_by_id=request.user.id
                    )
                return Response(serializer_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = WorkFlowTypeSerializer(instance, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowAccessViewSet(viewsets.ModelViewSet):
    queryset = WorkFlowAccess.objects.all()
    serializer_class = WorkFlowAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        # Fetch related WorkFlowType objects in bulk to avoid N+1 query issue
        wf_ids = [item['wf_id'] for item in response_data if 'wf_id' in item]
        work_flow_types = WorkFlowType.objects.filter(wf_id__in=wf_ids, is_active=True)
        work_flow_type_dict = {wf.wf_id: wf for wf in work_flow_types}
        # Update response data with related WorkFlowType objects
        for item in response_data:
            if 'wf_id' in item:
                wf_id = item['wf_id']
                item['work_flow_control'] = WorkFlowTypeSerializer(work_flow_type_dict[wf_id]).data
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            serializer = WorkFlowAccessSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                # Create WorkFlowDeptEmp objects
                for obj in data['data']:
                    for emp in obj['emp_ids']:
                        WorkFlowDeptEmp.objects.create(
                            wfa_id_id=serializer_data['wfa_id'],
                            type=obj['type'], emp_id=emp,
                            created_by_id=request.user.id
                        )
                return Response(serializer_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        arr = []

        queryset = self.get_queryset().filter(wfa_id=kwargs['pk']).first()
        serializer = self.serializer_class(queryset)
        serialize_data = serializer.data

        wfde = WorkFlowDeptEmp.objects.filter(wfa_id_id=kwargs['pk']).values('type', 'wfa_id_id').distinct()

        for obj in wfde:
            emp_list = WorkFlowDeptEmp.objects.filter(wfa_id_id=obj['wfa_id_id'], type=obj['type']).values_list(
                'emp_id', flat=True)
            arr.append({"type": obj['type'], "emp_id": list(emp_list)})

        serialize_data['dept_emp'] = arr

        serializer = {'records': serialize_data}
        if queryset is None:
            serializer = {'records': "No data available"}
        return Response(serializer)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data
            queries = self.get_queryset().filter(wfa_id=kwargs['pk']).first()
            serializer = WorkFlowAccessSerializer(queries, data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                serializer_data = serializer.data
                WorkFlowDeptEmp.objects.filter(wfa_id_id=data['wfa_id']).delete()
                for obj in data['data']:
                    for emp in obj['emp_ids']:
                        WorkFlowDeptEmp.objects.create(wfa_id_id=data['wfa_id'],type=obj['type'], emp_id=emp,created_by_id=request.user.id)
                return Response(serializer_data)
        return Response(False)

    @action(methods=['post'], detail=False, url_path='workflow_filter')
    def workflow_filter(self, request):
        try:
            data = request.data
            filter_data = WorkFlowAccess.objects.filter(dept_code_id=data['dept_code'], bill_type=data['bill_type']).values_list('wf_id_id', flat=True)
            workflow_controls = WorkFlowControl.objects.filter(wf_id_id__in=filter_data).order_by('wfc_id')
            serializer = WorkFlowControlSerializer(workflow_controls, many=True, context={'request': request})
            serializer_data = serializer.data
            max_level = workflow_controls.aggregate(Max('level'))
            for i in serializer_data:

                wfc_id = i['wfc_id']
                workflow_employee = WorkFlowEmployees.objects.filter(wfc_id=wfc_id).first()
                if workflow_employee:
                    emp_ids = workflow_employee.emp_id
                    employees = User.objects.filter(id__in=emp_ids).values('id', 'first_name')
                    employee_list = [{"id": employee['id'], "employee_name": employee['first_name']} for employee in employees]
                    i['wfe'] = [{"wfe_id": workflow_employee.wfe_id, "wfc_id": workflow_employee.wfc_id.wfc_id,"emp_id": employee_list}]
                else:
                    i['wfe'] = []
            return Response({'approvers':serializer_data,'max_level':max_level['level__max']})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class WorkFlowControlViewSet(viewsets.ModelViewSet):
    queryset = WorkFlowControl.objects.all()
    serializer_class = WorkFlowControlSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        # Fetch related WorkFlowType objects in bulk to avoid N+1 query issue
        wf_ids = [item['wf_id'] for item in response_data if 'wf_id' in item]
        work_flow_types = WorkFlowType.objects.filter(wf_id__in=wf_ids, is_active=True)
        work_flow_type_dict = {wf.wf_id: wf for wf in work_flow_types}
        # Update response data with related WorkFlowType objects
        for item in response_data:
            if 'wf_id' in item:
                wf_id = item['wf_id']
                item['wft'] = WorkFlowTypeSerializer(work_flow_type_dict[wf_id]).data
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = WorkFlowControlSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = WorkFlowControlSerializer(instance, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkFlowEmployeesViewSet(viewsets.ModelViewSet):
    queryset = WorkFlowEmployees.objects.all()
    serializer_class = WorkFlowEmployeesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        # Fetch related WorkFlowControl objects in bulk to avoid N+1 query issue
        wfc_ids = [item['wfc_id'] for item in response_data if 'wfc_id' in item]
        work_flow_controls = WorkFlowControl.objects.filter(wfc_id__in=wfc_ids)
        work_flow_control_dict = {wfc.wfc_id: wfc for wfc in work_flow_controls}
        # Update response data with related WorkFlowControl objects
        for item in response_data:
            if 'wfc_id' in item:
                wfc_id = item['wfc_id']
                item['wfc'] = WorkFlowControlSerializer(work_flow_control_dict[wfc_id]).data
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = WorkFlowEmployeesSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        serializer = WorkFlowEmployeesSerializer(instance, data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkFlowDaApproversViewSet(viewsets.ModelViewSet):
    queryset = WorkFlowDaApprovers.objects.all()
    serializer_class = WorkFlowDaApproversSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = WorkFlowDaApproversSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='create_wf_da_approval')
    def create_wf_da_approval(self, request, *args, **kwargs):
        try:
           with transaction.atomic():
               dil_id = request.data['dil_id']
               wf_id = request.data['wf_id']
               approval_list = request.data['approval']
               for item in approval_list:
                   data = {
                       'dil_id': dil_id,
                       'wf_id': wf_id,
                       'approver': item['approver'],
                       'level': item['level'],
                       'parallel': item['parallel'],
                       'emp_id': item['emp_id'],
                       'status': item['status'],
                   }
                   serializer = WorkFlowDaApproversSerializer(data=data, context={'request': request})
                   if serializer.is_valid():
                       serializer.save()
                   else:
                       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               return Response({'message': 'Workflow DA Approval created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='wf_da_approval_on_dil')
    def wf_da_approval_on_dil(self, request, *args, **kwargs):
        try:
            dil_id = request.data['dil_id']
            data = WorkFlowDaApprovers.objects.filter(dil_id=dil_id).values().order_by('wfd_id')
            for item in data:
                user_details = User.objects.get(id=item['emp_id'])
                user_serializer = EmployeeUserSerializer(user_details)
                item['emp_details'] = user_serializer.data
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
