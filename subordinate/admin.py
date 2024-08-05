from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(InsuranceScope)
admin.site.register(FreightBasis)
admin.site.register(DeliveryTerms)
admin.site.register(ModeOfShipment)
admin.site.register(PaymentStatus)
admin.site.register(SpecialPacking)
admin.site.register(ExportPackingRequirement)
admin.site.register(SpecialGSTRate)


