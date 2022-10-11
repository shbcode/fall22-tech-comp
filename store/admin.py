from django.contrib import admin
from .models import *
# Register your models here.
# admin.site.register(ShopUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(orderedproduct)
admin.site.register(ShippingAddress)