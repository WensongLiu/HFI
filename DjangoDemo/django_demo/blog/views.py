from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.

def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It's now %s.</body></html>" %now
    return HttpResponse(html)

def yellow(request):
    return render(request,'yellow.html')