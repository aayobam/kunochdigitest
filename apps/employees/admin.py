from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "date_created", "date_modified")
    readonly_fields = ("id", "date_created", "date_modified")