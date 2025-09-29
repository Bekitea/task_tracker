from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import CustomUser

def register_user(user_data):
    try:
        validate_password(user_data['password'])
    except ValidationError as e:
        raise ValidationError({'password': list(e.messages)})

    if CustomUser.objects.filter(username=user_data['username']).exists():
        raise ValidationError({'username': 'Пользователь с таким именем уже существует'})

    if CustomUser.objects.filter(email=user_data['email']).exists():
        raise ValidationError({'email': 'Пользователь с таким email уже существует'})

    user = CustomUser.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data.get('first_name', ''),
        last_name=user_data.get('last_name', '')
    )

    return user

def authenticate_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username
        }
    return None