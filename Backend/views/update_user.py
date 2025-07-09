from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from ..models import UserAccount
import traceback

@csrf_exempt
def update_user(request, user_id):
    if request.method == 'POST':
        try:
            # For multipart form, use request.POST and request.FILES
            user = UserAccount.objects.get(id=user_id)

            # Update text fields
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.role = request.POST.get('role', user.role)
            user.language = request.POST.get('language', user.language)
            user.phone_number = request.POST.get('phone_number', user.phone_number)

            # Optional: update password (hash it)
            password = request.POST.get('password')
            if password:
                user.password = make_password(password)

            # Optional: update image
            if 'profile_image' in request.FILES:
                user.profile_image = request.FILES['profile_image']

            user.save()
            return JsonResponse({'message': '✅ User updated successfully.'}, status=200)

        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Only PUT method allowed'}, status=405)
