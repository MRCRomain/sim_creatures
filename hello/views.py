import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "hello/home.html")


def hello_there(request, name):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def playground(request):
    return render(request, "hello/playground.html")

def parameters(request):
    return render(request, "hello/parameters.html")