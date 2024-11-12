from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    readonly_fields = ['id', 'last_login', 'date_joined', "password"]