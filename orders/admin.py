from django.contrib import admin

from .models import *


# Register your models here.

admin.site.register(Menu)
admin.site.register(Items)
admin.site.register(ShopCart)
admin.site.register(Order)