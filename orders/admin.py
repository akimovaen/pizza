from django.contrib import admin
from django.utils import timezone

from .models import *


# Register your models here.

def mark_as_complete(modeladmin, request, queryset):
    queryset.update(status='C')
    queryset.update(complete_time=timezone.now())
mark_as_complete.short_description = "Mark selected orders as complete"


class ShopCartInline(admin.TabularInline):
      model = ShopCart
      extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['number', 'placing_time', 'status', 'complete_time']
    ordering = ['-number']
    actions = [mark_as_complete]
    inlines = [
        ShopCartInline,
    ]


admin.site.register(Menu)
admin.site.register(Items)
admin.site.register(ShopCart)
admin.site.register(Order, OrderAdmin)