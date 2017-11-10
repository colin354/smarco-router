from django.db import models
from django.urls import reverse

# Create your models here.
class Device_info(models.Model):
    route_serial = models.CharField(max_length=50)
    vpn_status = models.CharField(max_length=50)
    software = models.CharField(max_length=50)
    hardware = models.CharField(max_length=50)
    route_ip = models.CharField(max_length=50)
    refresh = models.CharField(max_length=50,blank=True)

    #name = models.ForeignKey('users.User')

    def __str__(self):
        return self.route_serial

    def get_absolute_url(self):
        return reverse('vpn_server:detail', kwargs={'pk':self.pk})
