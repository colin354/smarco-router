# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from .forms import RegisterForm

def register(request):

    redirect_to = request.POST.get('next',request.GET.get('next',''))

    if request.method == 'POST':
        #request.POST is a dic.
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')

    else:
        form = RegisterForm()

    return render(request,'users/register.html',context={'form':form, 'next':redirect
        })

def index(request):
    return render(request,'index.html')
# Create your views here.
