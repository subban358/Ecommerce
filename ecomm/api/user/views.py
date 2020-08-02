from rest_framework import viewsets
from rest_framework.permission import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.viws.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import random
import re
# Create your views here.
def generate_session_token(length=10):
    return "".join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))

@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a POST request with valid parameters only'})
    username = request.POST.get('email')
    password = request.POST.get('password')

    #Validation

    if not re.match("[\w\.-]+@[\w\.-]+\.\w{2,4}", username): 
        return JsonResponse({'error':"enter a valid email address"})
    
    if len(password) < 6:
        return JsonResponse({'error': 'Password needs to be be at least 6 characters'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            user_dict = UserModel.objects.filter(email=username).values().first()
            user_dict.pop('password')

            if user.session_token != '0':
                user.session_token = '0'
                user.save()
                return JsonResponse({'error' : "Previous session exists"})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token' : token, 'user' : user_dict})
        else:
            return JsonResponse({'error' : "Invalid password"})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': "User does not exist"})

def signout(request, id):

    logout(request)

    UserModel = get_user_model()

    try:

        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': "Invalid user id"})
    
    return JsonResponse({'success':"logout success"})