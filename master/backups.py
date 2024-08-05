from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.db import transaction
from accounts.models import Department, SubDepartment
from .models import RoleMaster, ModuleMaster, UserRole, UserAccess
from django.contrib.auth import get_user_model
from django.db import IntegrityError
import pandas as pd

User = get_user_model()


# Create your views here.

class ImportDepartmentBulkData(APIView):
    def post(self, request, Format=None):
        file = self.request.FILES['file']
        if file:
            df = pd.read_csv(file)
            df = df.where(pd.notnull(df), None)
            df['OrgDepartment'] = df['OrgDepartment'].fillna(0).astype(str)
            for index, row in df.iterrows():
                department = Department.objects.filter(department_name=row['OrgDepartment'])
                if department.exists():
                    department.update(
                        department_name=row['OrgDepartment'],
                    )
                else:
                    Department.objects.create(
                        department_name=row['OrgDepartment'],
                    )
            return Response({'status': 'success', 'message': 'File uploaded successfully'})
        else:
            return Response("No file found")


class ImportUserBulkData(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            file = request.FILES.get('file')
            if file:
                df = pd.read_excel(file)
                df = df.where(pd.notnull(df), None)
                df['EmployeeNo'] = df['EmployeeNo'].fillna(0).astype(int)
                df['Name'] = df['Name'].fillna(0).astype(str)
                df['EMail'] = df['EMail'].fillna(0).astype(str)
                df['DomainId'] = df['DomainId'].fillna(0).astype(str)
                df['designation'] = df['designation'].fillna(0).astype(str)
                df['OrgDepartmentId'] = df['OrgDepartmentId'].fillna(0).astype(int)
                df['firstname'] = df['firstname'].fillna(0).astype(str)
                df['lastname'] = df['lastname'].fillna(0).astype(str)
                password = make_password('Yokogawa@12345')
                for index, row in df.iterrows():
                    departmentId = Department.objects.filter(id=row['OrgDepartmentId'])
                    sub_department = SubDepartment.objects.filter(department=departmentId.first())
                    user = User.objects.filter(username=row['DomainId'])
                    if user.exists():
                        user.update(
                            id=row['EmployeeNo'],
                            username=row['EmployeeNo'],
                            first_name=row['firstname'],
                            last_name=row['lastname'],
                            employee_no=row['DomainId'],
                            name=row['Name'],
                            email=row['EMail'],
                            designation=row['designation'],
                            department=departmentId.first(),
                            sub_department=sub_department.first(),
                            password=password
                        )
                    else:
                        User.objects.create(
                            id=row['EmployeeNo'],
                            username=row['EmployeeNo'],
                            first_name=row['firstname'],
                            last_name=row['lastname'],
                            employee_no=row['DomainId'],
                            name=row['Name'],
                            email=row['EMail'],
                            designation=row['designation'],
                            department=departmentId.first(),
                            sub_department=sub_department.first(),
                            password=password
                        )
                return Response({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': str(e)})


class ImportRoleMasterBulkData(APIView):
    def post(self, request, Format=None):
        file = self.request.FILES['file']
        try:
            if file:
                df = pd.read_csv(file)
                df = df.where(pd.notnull(df), None)
                df['role_name'] = df['role_name'].fillna(0).astype(str)
                df['is_active'] = df['is_active'].fillna(0).astype(bool)
                df['created_by_id'] = df['created_by_id'].fillna(0).astype(int)
                df['updated_by_id'] = df['updated_by_id'].fillna(0).astype(int)
                for index, row in df.iterrows():
                    role = RoleMaster.objects.filter(role_name=row['role_name'])
                    createBy = User.objects.filter(id=row['created_by_id'])
                    updateBy = User.objects.filter(id=row['updated_by_id'])
                    if role.exists():
                        role.update(
                            role_name=row['role_name'],
                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                    else:
                        RoleMaster.objects.create(
                            role_name=row['role_name'],
                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                return Response({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})


class ImportModuleMasterBulkData(APIView):
    def post(self, request):
        file = self.request.FILES['file']
        try:
            if file:
                df = pd.read_csv(file)
                df = df.where(pd.notnull(df), None)
                df['module_id'] = df['module_id'].fillna(0).astype(int)
                df['module_name'] = df['module_name'].fillna(0).astype(str)
                df['module_slug'] = df['module_slug'].fillna(0).astype(str)
                df['root'] = df['root'].fillna(0).astype(str)
                df['m_color'] = df['m_color'].fillna(0).astype(str)
                df['m_icon_name'] = df['m_icon_name'].fillna(0).astype(str)
                df['m_link'] = df['m_link'].fillna(0).astype(str)
                df['menu_flag'] = df['menu_flag'].fillna(0).astype(bool)
                df['sort_no'] = df['sort_no'].fillna(0).astype(int)
                df['is_active'] = df['is_active'].fillna(0).astype(bool)
                df['created_by_id'] = df['created_by_id'].fillna(0).astype(int)
                df['updated_by_id'] = df['updated_by_id'].fillna(0).astype(int)
                for index, row in df.iterrows():
                    module = ModuleMaster.objects.filter(module_id=row['module_id'])
                    createBy = User.objects.filter(id=row['created_by_id'])
                    updateBy = User.objects.filter(id=row['updated_by_id'])
                    if module.exists():
                        module.update(
                            module_id=row['module_id'],
                            module_name=row['module_name'],
                            module_slug=row['module_slug'],
                            root=row['root'],
                            m_color=row['m_color'],
                            m_icon_name=row['m_icon_name'],
                            m_link=row['m_link'],
                            menu_flag=row['menu_flag'],
                            sort_no=row['sort_no'],

                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                    else:
                        ModuleMaster.objects.create(
                            module_name=row['module_name'],
                            module_slug=row['module_slug'],
                            root=row['root'],
                            m_color=row['m_color'],
                            m_icon_name=row['m_icon_name'],
                            m_link=row['m_link'],
                            menu_flag=row['menu_flag'],
                            sort_no=row['sort_no'],

                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                return Response({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})


class ImportUserRoleBulkData(APIView):
    def post(self, request):
        file = self.request.FILES['file']
        try:
            if file:
                df = pd.read_csv(file)
                df = df.where(pd.notnull(df), None)
                df['role_id_id'] = df['role_id_id'].fillna(0).astype(int)
                df['module_id_id'] = df['module_id_id'].fillna(0).astype(int)
                df['add_access'] = df['add_access'].fillna(0).astype(bool)
                df['delete_access'] = df['delete_access'].fillna(0).astype(bool)
                df['view_access'] = df['view_access'].fillna(0).astype(bool)
                df['edit_access'] = df['edit_access'].fillna(0).astype(bool)
                df['is_active'] = df['is_active'].fillna(0).astype(bool)
                df['created_by_id'] = df['created_by_id'].fillna(0).astype(int)
                df['updated_by_id'] = df['updated_by_id'].fillna(0).astype(int)
                for index, row in df.iterrows():
                    User_role = UserRole.objects.filter(role_id=row['role_id_id'], module_id=row['module_id_id'])
                    role = RoleMaster.objects.filter(role_id=row['role_id_id'])
                    module = ModuleMaster.objects.filter(module_id=row['module_id_id'])
                    createBy = User.objects.filter(id=row['created_by_id'])
                    updateBy = User.objects.filter(id=row['updated_by_id'])
                    if User_role.exists():
                        User_role.update(
                            role_id=role.first(),
                            module_id=module.first(),
                            add_access=row['add_access'],
                            delete_access=row['delete_access'],
                            view_access=row['view_access'],
                            edit_access=row['edit_access'],
                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                    else:
                        UserRole.objects.create(
                            role_id=role.first(),
                            module_id=module.first(),
                            add_access=row['add_access'],
                            delete_access=row['delete_access'],
                            view_access=row['view_access'],
                            edit_access=row['edit_access'],

                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                return Response({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})


class ImportUserAccessBulkData(APIView):
    def post(self, request, Format=None):
        file = self.request.FILES['file']
        try:
            if file:
                df = pd.read_csv(file)
                df = df.where(pd.notnull(df), None)
                df['role_id_id'] = df['role_id_id'].fillna(0).astype(int)
                df['emp_id_id'] = df['emp_id_id'].fillna(0).astype(int)

                df['is_active'] = df['is_active'].fillna(0).astype(bool)
                df['created_by_id'] = df['created_by_id'].fillna(0).astype(int)
                df['updated_by_id'] = df['updated_by_id'].fillna(0).astype(int)
                for index, row in df.iterrows():
                    user_access = UserAccess.objects.filter(role_id=row['role_id_id'], emp_id=row['emp_id_id'])
                    role = RoleMaster.objects.filter(role_id=row['role_id_id'])
                    user = User.objects.filter(id=row['emp_id_id'])

                    createBy = User.objects.filter(id=row['created_by_id'])
                    updateBy = User.objects.filter(id=row['updated_by_id'])
                    if user_access.exists():
                        user_access.update(
                            role_id=role.first(),
                            emp_id=user.first(),
                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                    else:
                        UserAccess.objects.create(
                            role_id=role.first(),
                            emp_id=user.first(),
                            is_active=row['is_active'],
                            created_by=createBy.first(),
                            updated_by=updateBy.first()
                        )
                return Response({'status': 'success', 'message': 'File uploaded successfully'})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)})
