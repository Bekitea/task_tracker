from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from apps.users.serializers import RegistrationSerializer
from apps.users.services import register_user


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegistrationSerializer,
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'}
                }
            },
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'username': 'newuser',
                    'email': 'user@example.com',
                    'password': 'securepassword123',
                    'password_confirm': 'securepassword123',
                    'first_name': 'John',
                    'last_name': 'Doe'
                },
                request_only=True
            ),
            OpenApiExample(
                'Example response',
                value={
                    'message': 'Пользователь успешно зарегистрирован',
                    'user_id': 1,
                    'username': 'newuser'
                },
                response_only=True
            )
        ]
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = register_user(serializer.validated_data)
                return Response({
                    "message": "Пользователь успешно зарегистрирован",
                    "user_id": user.id,
                    "username": user.username
                }, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
