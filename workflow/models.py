from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from dispatch.models import DispatchInstruction
from accounts.models import SubDepartment

User = get_user_model()

# Create your models here.
''' The WorkFlowType is Super Model for WorkFlowControl 
and WorkFlowControl is Foreign Key of WorkFlowEmployees
'''


class WorkFlowType(models.Model):
    wf_id = models.AutoField(primary_key=True, unique=True)
    wf_name = models.CharField(max_length=150, null=True)
    slug_name = models.CharField(max_length=150, null=True)
    total_level = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowType'


class WorkFlowControl(models.Model):
    wfc_id = models.AutoField(primary_key=True, unique=True)
    wf_id = models.ForeignKey(WorkFlowType, null=True, related_name='wfc', on_delete=models.CASCADE)
    approver = models.CharField(max_length=150, null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    parallel = models.BooleanField(null=True, blank=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowControl'


class WorkFlowEmployees(models.Model):
    wfe_id = models.AutoField(primary_key=True, unique=True)
    wfc_id = models.ForeignKey(WorkFlowControl, null=True, related_name='wfe', on_delete=models.CASCADE)
    emp_type = models.CharField(max_length=150, null=True, blank=True)
    emp_id = ArrayField(models.IntegerField(null=True), default=list, blank=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowEmployees'


''' The WorkFlowAccess Model use WorkFLowDeptEmp '''


class WorkFlowAccess(models.Model):
    wfa_id = models.AutoField(primary_key=True, unique=True)
    wf_id = models.ForeignKey(WorkFlowType, null=True, on_delete=models.CASCADE)
    dept_code = models.ForeignKey(SubDepartment, null=True, on_delete=models.CASCADE)
    auth_list = ArrayField(models.CharField(max_length=50, null=True), default=list, blank=True)
    bill_type = models.CharField(max_length=150, null=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowAccess'


class WorkFlowDeptEmp(models.Model):
    wfde_id = models.AutoField(primary_key=True, unique=True)
    wfa_id = models.ForeignKey(WorkFlowAccess, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, null=True)
    emp_id = models.IntegerField(null=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowDeptEmp'


class WorkFlowDaApprovers(models.Model):
    wfd_id = models.AutoField(primary_key=True, unique=True)
    dil_id = models.ForeignKey(DispatchInstruction, null=True, on_delete=models.CASCADE)
    wf_id = models.ForeignKey(WorkFlowType, null=True, on_delete=models.CASCADE)
    approver = models.CharField(max_length=150, null=True)
    level = models.IntegerField(null=True)
    parallel = models.BooleanField(null=True)
    emp_id = models.IntegerField(null=True)
    status = models.CharField(max_length=150, null=True)

    created_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'WorkflowDaApprovers'
