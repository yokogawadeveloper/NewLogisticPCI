from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class RoleMaster(models.Model):
    role_id = models.AutoField(primary_key=True, unique=True)
    role_name = models.CharField(max_length=30, null=True)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        db_table = "RoleMaster"


class ModuleMaster(models.Model):
    module_id = models.AutoField(primary_key=True, unique=True)
    module_name = models.CharField(max_length=100, null=True)
    module_slug = models.CharField(max_length=100, null=True)
    root = models.CharField(max_length=100, null=True)
    m_color = models.CharField(max_length=100, null=True)
    m_icon_name = models.CharField(max_length=100, null=True)
    m_link = models.CharField(max_length=100, null=True)
    menu_flag = models.BooleanField(default=True)
    sort_no = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "ModuleMaster"


class UserRole(models.Model):
    user_id = models.AutoField(primary_key=True, unique=True)
    role_id = models.ForeignKey(RoleMaster, null=True, related_name='RoleMasterTable', on_delete=models.CASCADE)
    module_id = models.ForeignKey(ModuleMaster, null=True, related_name='ModuleMasterTable', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    add_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)
    view_access = models.BooleanField(default=False)
    edit_access = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    objects = models.Manager()

    class Meta:
        db_table = "UserRole"


class UserAccess(models.Model):
    emp_id = models.ForeignKey(User, null=True, related_name="EmployeeUser", on_delete=models.CASCADE)
    role_id = models.ForeignKey(RoleMaster, null=True, related_name='RoleMaster', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = "UserAccess"

