import markdown
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
import demjson
import json
import time
from .models import Device_info
from .forms import DeviceinfoForm


def index(request):
    device_list = Device_info.objects.all()
    return render(request,'vpn_server/index.html',context={
        'title':'vpn_server',
        'device_list': device_list
        })

def detail(request, pk):
    device_info = get_object_or_404(Device_info,pk=pk)
    form = DeviceinfoForm()
    context = {'device_info':device_info,'form':form}
    return render(request,'vpn_server/detail.html',context=context)
    
def route_status_ctl(request, device_info_pk):
    device_info = get_object_or_404(Device_info, pk=device_info_pk)
    if request.method == 'POST':
        form = DeviceinfoForm(request.POST)
        if form.is_valid():
            if device_info.vpn_status=="on":
                device_info.vpn_status = "off"
            elif device_info.vpn_status=="off":
                device_info.vpn_status = "on"
            device_info.save()
            return redirect(device_info)
        else:
            device_list = Device_info.objects.all()
            context = {'device_info':device_info,
                    'form':form,
                    'device_list':device_list
                    }
            print("no hello")
            return render(request, 'vpn_server/detail.html', context=context)
    return redirect(device_info)


def vpn_status_ctl(request, device_info_pk):
    
    device_info = get_object_or_404(Device_info, pk=device_info_pk)
    print(device_info.vpn_status)
    if device_info.vpn_status=="on":
        device_info.vpn_status = "off"
    elif device_info.vpn_status=="off":
        device_info.vpn_status = "on"
    
    device_info.save()
    device_list = Device_info.objects.all()
    return render(request,'vpn_server/index.html',context={
        'title':'vpn_server',
        'device_list': device_list
        })

router_devices = dict()

def _create_device_info(sn):
    return {
        'id':sn,
        'vpn_status':"off",
        'software':'unkown',
        'hardware':'unkown',
        'ip':'unkown',
        'refresh': 0,
    }

def _get_device_info(sn):
    return router_devices.get(sn, _create_device_info(sn))

def _register_device_info(info):
    device_info,created = Device_info.objects.get_or_create(route_serial=info['id'])
    if created:
        device_info.route_serial = info['id']
        device_info.vpn_status = "off"
        device_info.software = info['software']
        device_info.hardware = info['hardware']
        device_info.route_ip = info['ip']
        device_info.refresh = time.time()
        device_info.save()
        print("creat")
    else:
        print("n creat")
        device_info.refresh = time.time()
        device_info.save()

    sn = info['id']
    ret = router_devices.get(sn, _create_device_info(sn))

    for field in ["software", "hardware", 'ip']:
        ret[field] = info[field]
    ret['refresh'] = time.time()
    if sn not in router_devices:
        router_devices[sn] = ret


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@require_http_methods(["POST", "GET"])
def devices(request):
    if request.method == "GET":
        device_info_obj = Device_info.objects.all()
        device_info = serializers.serialize("json",device_info_obj)
        device_info_json = demjson.decode(device_info)
        return HttpResponse(json.dumps(device_info_json))
        #return HttpResponse(json.dumps(router_devices))
    elif request.method == "POST":
        info = dict()
        for field in ['id', 'software', 'hardware']:
            info[field] = request.POST.get(field, "")
        info['ip'] = get_client_ip(request)
        print(info)
        _register_device_info(info)
        device_info = serializers.serialize("json",Device_info.objects.filter(route_serial=info['id']))
        #print(((demjson.decode(device_info))[0]['fields']))
        return HttpResponse(json.dumps(demjson.decode(device_info)))
        #return HttpResponse(json.dumps(_get_device_info(info['id'])))

@require_http_methods(["GET", "POST"])
def device_info(request, device_id=""):
    if request.method == "POST":
        device_info_obj = Device_info.objects.get(route_serial=device_id)
        status = request.POST.get('vpn_status', '')
        if (status=='on' or status == 'off') and device_info_obj:
            device_info_obj.vpn_status = status
            device_info_obj.save()
            print("set device (%s) vpn status to %s" % (device_id, status));

    device_info_obj = Device_info.objects.filter(route_serial=device_id)
    device_info = serializers.serialize("json",device_info_obj)
    device_info_json = demjson.decode(device_info)
    return HttpResponse(json.dumps((device_info_json[0]['fields'])))
    #device_info = get_object_or_404(Device_info,route_serial=device_id)
    #form = DeviceinfoForm()
    #context = {'device_info':device_info,'device_info_json':(device_info_json[0]['fields']),'form':form}
    #return render(request,'vpn_server/device_info.html',context=context)
# Create your views here.


