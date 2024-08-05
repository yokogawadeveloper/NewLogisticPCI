from django.contrib import admin
from .models import *


# Register your models here.
class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')


admin.site.register(Department)
admin.site.register(SubDepartment)
admin.site.register(EmployeeUser, EmployeeUserAdmin)
