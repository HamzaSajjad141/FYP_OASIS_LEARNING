from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required(login_url = 'Login')
def Home(request):
    return render(request,"home.html")


def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        print(username, passw)
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'success', 'url': 'Home'})
        else:
            return JsonResponse({'message': 'Invalid Credentials'})

    return render(request, "login.html")


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

def video(request):
    return render(request,"video.html")

def Dashboard(request):
    return render(request,"Dashboard.html")


def Adduser(request):
    return render(request,"Adduser.html")

def UpdateUser(request):
    return render(request,"Updateuser.html")

def DeleteUser(request):
    return render(request,"deleteuser.html")

def Users(request):
    return render(request,"users.html")


def managecomplaints(request):
    return render(request,"managecomplaints.html")






import openai

openai_api_key = "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"
openai.api_key = openai_api_key

def ask_openai(userMessage):
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": userMessage}
    ])
    
    answer = completion.choices[0].message.content
    
    return answer

def getResponse(request):
    userMessage = request.GET.get('userMessage')
    
    completion = ask_openai(userMessage)
    print(completion)
    
    return HttpResponse(completion)