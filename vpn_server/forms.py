from django import forms
from .models import Device_info

class DeviceinfoForm(forms.Form):
    vpn_status = forms.CharField(max_length=50,label="vpn_status",required=False)    
