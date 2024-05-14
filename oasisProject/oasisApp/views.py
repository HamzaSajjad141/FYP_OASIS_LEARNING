from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Complaint , History
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect



# Decorator to check if user is superuser
def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_superuser,
        login_url='Login'
    )(view_func)
    return decorated_view_func

@login_required(login_url = 'Login')
def Home(request):
    return render(request,"home.html")


def Login(request):
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to the home page or any other appropriate page
        if request.user.is_superuser:
            return redirect('Dashboard')  # Redirect to admin dashboard
        else:
            return redirect('Home')  # Redirect to home page for regular users

    if request.method == 'POST':
        username = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return JsonResponse({'message': 'success', 'url': 'Dashboard'})  # Redirect to admin dashboard
            else:
                return JsonResponse({'message': 'success', 'url': 'Home'})  # Redirect to home page for regular users
        else:
            return JsonResponse({'message': 'Invalid Credentials','url': ''})

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

@login_required(login_url='Login')
def Logout(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='Login')
def AboutUs(request):
    return render(request,"About.html")


@login_required(login_url='Login')
def ContactUs(request):
    
    
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save the complaint in the database
        complaint = Complaint.objects.create(
            user=request.user,
            description=message
        )
        # You might want to add additional fields like name and email to the Complaint model
        # depending on your requirements
        
        # Redirect the user to a thank you page or any other appropriate page
        return redirect('Home')

    # Filter complaints based on the currently logged-in user
    user_complaints_with_responses = Complaint.objects.filter(user=request.user, respond__isnull=False)

    return render(request, "Contact.html", {'user_complaints_with_responses': user_complaints_with_responses})

@login_required(login_url='Login')
def history(request):
    # Retrieve all history objects from the database
    history_entries = History.objects.filter(user=request.user)
    return render(request, "Viewhistory.html", {'history_entries': history_entries})


def Chat(request):
    return render(request,"Chat.html")

def video(request):
    return render(request,"video.html")



@superuser_required
def Dashboard(request):
    

    
    regular_users_count = User.objects.filter(is_superuser=False).count()
    
    # Fetch superusers
    admin = User.objects.filter(is_superuser=True)
    
    context = {
        'regular_users_count': regular_users_count,
        'superusers': admin
    }
    return render(request, "Dashboard.html", context)



@superuser_required
def Adduser(request):
    if request.method == 'POST':
        usrname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        print(usrname,email,pass1,pass2)
        
        if User.objects.filter(username=usrname).exists():
            return JsonResponse({'error': 'Username is already taken. Please choose a different one.'})
        else:
            Reg_User = User.objects.create_user(usrname,email,pass1)
            Reg_User.save()
            messages.success(request, 'User added successfully!')
            return render(request, "Dashboard.html")

    return render(request,"Adduser.html")


@superuser_required
def UpdateUser(request):
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        new_email = request.POST.get('email')

        try:
            # Get the user object by username
            user = User.objects.get(username=username)
            # Update the user's email
            user.email = new_email
            user.save()
            # Redirect to Dashboard or any other appropriate page
            return redirect('Dashboard')
        except User.DoesNotExist:
            # Handle if the user does not exist
            # You can render a message or redirect to the same page with an error message
            return render(request, 'updateuser.html', {'error_message': 'User does not exist.'})

    # If request method is not POST, render the updateuser.html template
    return render(request, "updateuser.html")


@superuser_required
def DeleteUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        confirmation = request.POST.get('confirmation')

        # Check if the confirmation matches the required string
        if confirmation != 'DELETE':
            messages.error(request, 'Confirmation string incorrect. Please type "DELETE" to confirm.')
            return redirect('DeleteUser')

        try:
            # Get the user object
            user = User.objects.get(username=username)
            # Delete the user
            user.delete()
            messages.success(request, f'User {username} deleted successfully!')
            return redirect('Dashboard')
        except User.DoesNotExist:
            messages.error(request, f'User with username {username} does not exist.')
            return redirect('DeleteUser')

    return render(request, "deleteuser.html")


@superuser_required
def Users(request):
    # Fetch regular users from the database, excluding superusers
    regular_users = User.objects.filter(is_superuser=False)
    
    context = {
        'users': regular_users
    }
    return render(request, "users.html", context)




@superuser_required
def managecomplaints(request):
    complaints = Complaint.objects.all()  # Fetch all complaints from the database

    context = {
        'complaints': complaints
    }
    return render(request, "managecomplaints.html", context)




@superuser_required
def respond_complaint_view(request, complaint_id):
    # Retrieve the complaint object corresponding to the complaint_id
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if request.method == 'POST':
        # Process the form data submitted for responding to the complaint
        response_text = request.POST.get('response', '')  # Assuming your form field name is 'response'
        
        # Save the response to the complaint
        complaint.respond = response_text
        complaint.status = 'Responded'
        complaint.save()
        
        # Redirect the user to a success page or any other relevant page
        return HttpResponseRedirect('/Dashboard/')  # Redirect to Dashboard after responding
        
    # If the request method is GET, render the respondcomplaint.html template
    return render(request, 'respondcomplaint.html', {'complaint': complaint})


import os 
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

from transformers import AutoProcessor, SeamlessM4Tv2Model
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

import requests
import time

def ask_openai(userMessage):
    userMessage = "Can you help me with the question " + userMessage + "? Also, could you suggest some related topics or areas for further exploration?"
    
    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
    azure_openai_development = os.getenv("AZURE_OPENAI_DEVELOPMENT") 
    
    #azue openai
    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key= azure_openai_key,
        api_version= "2024-02-15-preview"            
    )
    
    system_message = "You are an AI assistant that helps people find information."
    
    messages_array = [{"role": "system", "content": system_message}]
        
    # Add code to send request...
    # Send request to Azure OpenAI model
    
    #ask gpt to generate prompt
    messages_array.append({"role": "user", "content": userMessage})
    
    response = client.chat.completions.create(
        model= azure_openai_development,
        temperature= 0.7,
        max_tokens= 1200,
        messages= messages_array
    )
    generated_answer = response.choices[0].message.content
        
    #Add generated text to messages array
    messages_array.append({"role": "system", "content": generated_answer})
    
    return generated_answer

def translation(text_to_translate, lan):

    text_inputs = processor(text_to_translate, src_lang="eng", return_tensors="pt")

    # from text
    output_tokens = model.generate(**text_inputs, tgt_lang = lan, generate_speech=False)
    translated_text_from_text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)

    print(translated_text_from_text)
    return translated_text_from_text
    
def video_gen(text_to_video, language, user_voice, image):
    if language == "eng" and user_voice == "Male":
        voice = "en-US-AndrewMultilingualNeural"
    elif language == "eng" and user_voice == "Female":
        voice = "en-US-JennyNeural"
    elif language == "urd" and user_voice == "Male":
        voice = "ur-PK-AsadNeural"
    elif language == "urd" and user_voice == "Female":
        voice = "ur-PK-UzmaNeural"
    elif language == "hin" and user_voice == "Male":
        voice = "hi-IN-MadhurNeural"
    elif language == "hin" and user_voice == "Female":
        voice = "hi-IN-KavyaNeural"
        
        
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "microsoft",
                "voice_id": voice
            },
            "input": str(text_to_video)
        },
        "config": {
            "fluent": "false",
            "pad_audio": "0.0"
        },
        "source_url": image
    }
    headers = {
        "Authorization": "Basic ZjIwMDMyOUBjZmQubnUuZWR1LnBr:AR9LVrGhgNLbT5ilCU04U",
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
    headers = {"Authorization": "Basic ZjIwMDMyOUBjZmQubnUuZWR1LnBr:AR9LVrGhgNLbT5ilCU04U",
               "accept": "application/json"}
    response = requests.get(url, headers=headers)
    print('Second Response: ',response.text)
    
    # Parse the JSON response
    response_json = response.json()

    # Extract the result_url from the response JSON
    result_url = response_json.get("result_url")
    return result_url

    
#cloudinary imports
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Import the CloudinaryImage and CloudinaryVideo methods for the simplified syntax used in this guide
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo

#Configuration
cloudinary.config(
    cloud_name = "dsogv65gk",
    api_key = "542235843671834",
    api_secret = "ht5pCWElYBkWVnb1J6HHB04lP0Q",
)

def upload_image(request):
    if request.method == 'POST':
        # Get the form data
        user_message = request.POST.get('userMessage')
        language = request.POST.get('languageSelect')
        accent = request.POST.get('accentSelect')
        user_image = request.FILES.get('userImage')
        
        print("User Message: ",user_message)
        print("Language: ",language)
        print("Accent: ", accent)
        print("Image: ",user_image)

        
        # Upload an image
        upload_result = cloudinary.uploader.upload(user_image, public_id="shoes")
        print("Image_url: ", upload_result["secure_url"])
        
        completion = ask_openai(user_message)
        print(completion)
    
        translated_text = translation(completion, language)
        print(translated_text)
           
        id_get = video_gen(translated_text, language, accent, upload_result["secure_url"])
        print(id_get)
        
        time.sleep(30)
        
        get_vid = get_video(id_get)
        print(get_vid)
        
        history_entry = History.objects.create(
            user=request.user,
            query_text=user_message,
            translated_text=translated_text,
            video_url=get_vid
        )
    return render(request, 'video.html', {'video_url': get_vid, 'translated_text': translated_text})