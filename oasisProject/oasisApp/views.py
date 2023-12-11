from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required(login_url = 'Login')
def Home(request):
    return render(request,"home.html")


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        print(username,passw)
        user = authenticate(request, username=username, password=passw)
        if user is not None :
            login(request,user)
            return redirect('Home')
        else:
            return HttpResponse("Invalid Credentials")

    return render(request,"login.html")


def Register(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        print(usrname,email,pass1,pass2)
        
        if User.objects.filter(username=usrname).exists():
            return HttpResponse("Username is already taken. Please choose a different one.")
        else:
            Reg_User = User.objects.create_user(usrname,email,pass1)
            Reg_User.save()
            return redirect('Login')

        

    
    
    
    return render(request,"Register.html")

def Logout(request):
    logout(request)
    return redirect('Login')

def AboutUs(request):
    return render(request,"About.html")


def ContactUs(request):
    return render(request,"Contact.html")


def history(request):
    return render(request,"Viewhistory.html")


def Chat(request):
    return render(request,"Chat.html")

def Dashboard(request):
    return render(request,"Dashboard.html")