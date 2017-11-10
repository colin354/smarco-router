from django.contrib import admin
from .models import Device_info

class DeviceAdmin(admin.ModelAdmin):
    list_display = ['route_serial','vpn_status','software','hardware','route_ip']
admin.site.register(Device_info,DeviceAdmin)
# Register your models here.
