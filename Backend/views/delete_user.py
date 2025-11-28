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



@csrf_exempt
def delete_user(request, user_id):
    if request.method == 'DELETE':
        try:
            user = UserAccount.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'message': '✅ User deleted successfully.'}, status=200)
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only DELETE method allowed'}, status=405)

