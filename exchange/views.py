from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    return render(request, 'exchange/index.html')

def explore_index(request, args):
    return render(request, 'exchange/explore/index.html')

def participate_index(request, args):
    return render(request, 'exchange/participate/index.html')
