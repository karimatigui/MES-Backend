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
from ..models import IonAPICredentials 
import traceback
from django.core.mail import send_mail



@csrf_exempt  # Only for testing! In production, use CSRF protection
def create_ionapi_credentials(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            credentials = IonAPICredentials(
                ti = data.get('ti', ''),
                cn = data.get('cn', ''),
                dt = data.get('dt', ''),
                ci = data.get('ci', ''),
                cs = data.get('cs', ''),
                iu = data.get('iu', ''),
                pu = data.get('pu', ''),
                oa = data.get('oa', ''),
                ot = data.get('ot', ''),
                or_field = data.get('or', ''),
                sc = data.get('sc', []),
                ev = data.get('ev', ''),
                v = data.get('v', ''),
                company = data.get('company', '')
            )
            credentials.save()

            return JsonResponse({
                'message': 'IonAPI credentials saved successfully!',
                'data': {
                    'id': credentials.id,
                    'cn': credentials.cn,
                    'ti': credentials.ti
                }
            }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)