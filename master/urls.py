from django.urls import path
from .backups import *

urlpatterns = [
    path('import_department', ImportDepartmentBulkData.as_view(), name='import_department'),
    path('import_user', ImportUserBulkData.as_view(), name='import_user'),
    path('import_role', ImportRoleMasterBulkData.as_view(), name='import_role'),
    path('import_module', ImportModuleMasterBulkData.as_view(), name='import_module'),
    path('import_user_role', ImportUserRoleBulkData.as_view(), name='import_user_role'),
    path('import_user_access', ImportUserAccessBulkData.as_view(), name='import_user_access'),
]
