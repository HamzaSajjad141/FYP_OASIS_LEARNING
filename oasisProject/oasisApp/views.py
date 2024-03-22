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

from transformers import AutoProcessor, SeamlessM4Tv2Model
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

import requests
import time

def ask_openai(userMessage):
    # completion = openai.chat.completions.create(
    # model="gpt-3.5-turbo",
    # messages=[
    #     {"role": "system", "content": "You are a helpful assistant."},
    #     {"role": "user", "content": userMessage}
    # ])
    
    # answer = completion.choices[0].message.content
    
    answer = '''Function overloading is a programming concept in which multiple functions can have the same name but different parameters or argument lists. This allows you to define multiple functions with the same name within the same scope, but with each function having different parameters or different types of parameters.
    When you call an overloaded function, the compiler determines which version of the function to execute based on the number and types of arguments provided in the function call. This allows you to create more flexible and versatile code by providing multiple ways to call a function with different sets of parameters. 
    Function overloading is commonly used in object-oriented programming languages like C++, Java, and C#. It helps improve code readability, reusability, and maintainability by allowing developers to define functions that perform similar tasks but operate on different types of data or accept different numbers of arguments.'''
    return answer

def translation(text_to_translate):

    text_inputs = processor(text_to_translate, src_lang="eng", return_tensors="pt")

    # from text
    output_tokens = model.generate(**text_inputs, tgt_lang="fra", generate_speech=False)
    translated_text_from_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    print(translated_text_from_text)
    return translated_text_from_text
    
def video_gen(text_to_video):

    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": "en-US-GuyNeural"
            },
            "input": text_to_video
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": "https://assets.mycast.io/actor_images/actor-johnny-sins-75125_large.jpg?1586055334"
    }
    headers = {
        "Authorization": "Basic emFlZW0ubXVoYW1tYWQueWFzZWVuMjBAZ21haWwuY29t:s-WqghqPlX0MpIIAgXqzo",
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print('First Response: ',response.text)
    
    response_json = response.json()
    talk_id = response_json.get("id")
    return talk_id
    
def get_video(id):
    url = "https://api.d-id.com/talks/" + id
    headers = {"Authorization": "Basic emFlZW0ubXVoYW1tYWQueWFzZWVuMjBAZ21haWwuY29t:s-WqghqPlX0MpIIAgXqzo",
               "accept": "application/json"}
    response = requests.get(url, headers=headers)
    print('Second Response: ',response.text)
    
    # Parse the JSON response
    response_json = response.json()

    # Extract the result_url from the response JSON
    result_url = response_json.get("result_url")
    return result_url
    
def getResponse(request):
    userMessage = request.GET.get('userMessage')
    
    completion = ask_openai(userMessage)
    print(completion)
    
    translated_text = translation(completion)
    print(translated_text)    
    
    id_get = video_gen(translated_text)
    print(id_get)
    
    time.sleep(60)
    
    get_vid = get_video(id_get)
    print(get_vid)

    return HttpResponse(get_vid)