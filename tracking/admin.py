from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(TruckType)
admin.site.register(TrackingTransportation)
admin.site.register(TruckRequest)
admin.site.register(TruckRequestTypesList)
admin.site.register(TruckList)
admin.site.register(TruckDilMappingDetails)
admin.site.register(TruckLoadingDetails)
admin.site.register(DeliveryChallan)
admin.site.register(DCInvoiceDetails)
admin.site.register(InvoiceChequeDetails)

