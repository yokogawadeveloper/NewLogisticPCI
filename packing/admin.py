from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(BoxType)
admin.site.register(BoxSize)
admin.site.register(BoxDetails)
admin.site.register(BoxDetailsFile)
admin.site.register(ItemPacking)
admin.site.register(ItemPackingInline)
admin.site.register(PackingPrice)
