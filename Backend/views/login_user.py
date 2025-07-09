from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from ..models import UserAccount

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = UserAccount.objects.get(username=username)
        if check_password(password, user.password):
            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'language': user.language,
                    'phone_number': user.phone_number,
                    'created_at': user.created_at
                }
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
    except UserAccount.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
