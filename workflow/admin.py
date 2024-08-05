from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(WorkFlowType)
admin.site.register(WorkFlowControl)
admin.site.register(WorkFlowEmployees)
admin.site.register(WorkFlowDaApprovers)
admin.site.register(WorkFlowAccess)
