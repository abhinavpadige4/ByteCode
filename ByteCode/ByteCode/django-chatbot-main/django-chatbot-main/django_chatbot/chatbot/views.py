import os
from dotenv import load_dotenv
import openai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Load OpenAI API Key
load_dotenv()
openai.api_key = os.getenv(
    "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"
)


# Function to interact with OpenAI
def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant."
            }, {
                "role": "user",
                "content": message
            }])
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error: {str(e)}"


# Chatbot View (Requires Authentication)
@login_required
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        if not message:
            return JsonResponse({'error': 'Message cannot be empty'},
                                status=400)

        response = ask_openai(message)

        chat = Chat(user=request.user,
                    message=message,
                    response=response,
                    created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})


# Login View
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            return render(request, 'login.html',
                          {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')


# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html',
                          {'error_message': 'Username already exists'})

        if password1 != password2:
            return render(request, 'register.html',
                          {'error_message': 'Passwords do not match'})

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password1)
        auth.login(request, user)
        return redirect('chatbot')

    return render(request, 'register.html')


# Logout View
def logout(request):
    auth.logout(request)
    return redirect('login')
