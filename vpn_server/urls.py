from django.conf.urls import url
from . import views

app_name = 'vpn_server'
urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^device_info/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
            url(r'^route_status/device_info/(?P<device_info_pk>[0-9]+)/$', views.route_status_ctl, name='route_status_ctl'),
            url(r'^vpn_status/device_info/(?P<device_info_pk>[0-9]+)/$', views.vpn_status_ctl, name='vpn_status_ctl'),
            url(r'^devices/$',views.devices,name="devices"),
            url(r'^devices/(?P<device_id>[0-9-]{15})/$',views.device_info,name="device_info"),
        ]

