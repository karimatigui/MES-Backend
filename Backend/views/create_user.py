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
from .generate_random_password import generate_random_password


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']

            # ✅ Check if user already exists
            if UserAccount.objects.filter(email=email).exists():
                return JsonResponse(
                    {'error': f"A user with email '{email}' already exists."},
                    status=409  # Conflict
                )
            if UserAccount.objects.filter(username=data['username']).exists():
                return JsonResponse(
                    {'error': 'Username already exists.'},
                    status=409
                )

            # Proceed to create user
            plain_password = generate_random_password()
            hashed_password = make_password(plain_password)

            user = UserAccount.objects.create(
                username=data['username'],
                email=email,
                role=data['role'],
                language=data['language'],
                phone_number=data['phone_number'],
                password=hashed_password,
            )

            # ✅ Send email
            subject = '✅ Your ZUM-IT MES Account Login'
            login_url = 'http://mes-smart-factory.tn/#/login'  # Customize this
            message = f"""
Hello {user.username},

Welcome! Your account has been created successfully.

🔐 Your login credentials:
- Username: {user.username}
- Password: {plain_password}

🔗 Login here: {login_url}

Please change your password after logging in.

Best regards,  
ZUM IT Team
"""
            try:
                send_mail(
                    subject,
                    message,
                    'karim01atigui@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as mail_error:
                print("❌ Failed to send email:", mail_error)
                return JsonResponse({'error': 'Email failed to send.'}, status=500)

            return JsonResponse({
                'message': '✅ User created and email sent.',
                'username': user.username
            }, status=201)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
