from django.shortcuts import render
from django.http import HttpResponse
from blog.forms import SignupForm
from blog.models import Users
import datetime

# Create your views here.

def home(request):
    now = datetime.datetime.now()
    html = "<html><body>It's now %s.</body></html>" %now
    return HttpResponse(html)

def yellow(request):
    return render(request,'yellow.html', {}, status = "200")

def welcome(request):
    now = datetime.datetime.now()
    return render(request,'welcome.html', {'time': now}, status = '200')

def signUp(request):
    path = request.get_full_path()
    print(path)
    if request.method=='POST':
        form=SignupForm(data=request.POST)
        if form.is_valid():
            email = form.getEmail()
            print(email)
            return redirect(request, 'welcome.html', {'email':email}, status ='200')
    else:
        form=SignupForm()
    return render(request,'signUp.html',locals())
