from django.http import JsonResponse
from Backend.models import UserAccount

def get_user_data(request, user_id):
    if request.method == 'GET':
        try:
            user = UserAccount.objects.get(id=user_id)

            # Build full response
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'language': user.language,
                'phone_number': user.phone_number,
                'profile_image': f"/media/{user.profile_image}" if user.profile_image else ''
            }

            return JsonResponse(user_data, safe=False)
        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    return JsonResponse({'error': 'Only GET method allowed'}, status=405)
