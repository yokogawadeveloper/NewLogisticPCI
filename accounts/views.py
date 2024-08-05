from rest_framework import status, generics
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import timedelta
from .models import ActiveUser
from .decorators import *
from .serializers import *
from master.models import *


User = get_user_model()


# Create view here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmployeeTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        user = None
        serializer = self.get_serializer(data=request.data)
        if User.objects.filter(username=request.data['username']).exists():
            try:
                user = User.objects.get(username=request.data['username'])
                user_id = User.objects.filter(username=request.data['username']).values('id')[0]['id']
                role_id = UserAccess.objects.filter(emp_id=user_id).values('role_id_id')
                if role_id.exists():
                    role_id = role_id[0]['role_id_id']
                    role_id = RoleMaster.objects.filter(role_id=role_id).values('role_id')[0]['role_id']
                    user.role = role_id
                else:
                    user.role = None
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            # Getting menu for user role
            menu_response = get_user_menu(user.role)
            root_list = get_root_list(user.role)
            # Returning combined response
            return Response({
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'employee_no': user.employee_no,
                    'name': user.name,
                    'email': user.email,
                    'designation': user.designation,
                    'is_sub_department_head': user.is_sub_department_head,
                    'is_department_head': user.is_department_head,
                    'department': user.department.id if user.department else None,
                    'subDepartment': user.sub_department.id if user.sub_department else None,
                    'role': user.role if user.role else 'No Role Assigned',
                },
                'menu': menu_response,
                'sub_menu': root_list
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class EmployeeUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = EmployeeUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter(is_active=True)
        return query_set

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True, context={'request': request})
        serializer_data = serializer.data
        return Response(serializer_data)


class SubDepartmentViewSet(viewsets.ModelViewSet):
    queryset = SubDepartment.objects.all()
    serializer_class = SubDepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query_set = self.queryset.filter()
        return query_set

    def list(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.serializer_class(query_set, many=True, context={'request': request})
        serializer_data = serializer.data
        return Response(serializer_data)


class ActiveUserCountView(APIView):
    def get(self, request):
        now = timezone.now()
        time_threshold = now - timedelta(minutes=5)
        active_users_count = ActiveUser.objects.filter(last_activity__gte=time_threshold).count()
        return Response({'active_users_count': active_users_count})