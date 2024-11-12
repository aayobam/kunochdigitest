from django.contrib import admin
from .models import Order


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ("customer", "item_name", "quantity", "price", "total_price")
    readonly_fields = ("total_price",)