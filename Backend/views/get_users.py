# views.py
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
import requests  # type: ignore
from Backend.utils.token_manager import get_mingle_token
from django.http import JsonResponse
from rest_framework import status
from Backend.models import IonAPICredentials
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
import json
import string
import random
from ..models import UserAccount
import traceback
from django.core.mail import send_mail



def get_users(request):
    if request.method == 'GET':
        users = UserAccount.objects.all().values(
            'id', 'username', 'email', 'role', 'language', 'phone_number', 'created_at','password' , 'profile_image'
        )
        return JsonResponse(list(users), safe=False)
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)