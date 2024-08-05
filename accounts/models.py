from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class Department(models.Model):
    department_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Department'
        verbose_name_plural = 'Department'

    def __str__(self):
        return self.department_name


class SubDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    sub_department_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'SubDepartment'
        verbose_name_plural = 'SubDepartment'

    def __str__(self):
        return self.sub_department_name


class EmployeeUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            password = 'Yokogawa@12345'
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)


class EmployeeUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    employee_no = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    sub_department = models.ForeignKey(SubDepartment, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_sub_department_head = models.BooleanField(default=False)
    is_department_head = models.BooleanField(default=False)

    objects = EmployeeUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'EmployeeUser'
        verbose_name_plural = 'EmployeeUser'

    def __str__(self):
        return self.username
