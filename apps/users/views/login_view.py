from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import LoginSerializer
from apps.users.services import authenticate_user


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                    'user_id': {'type': 'integer'},
                    'username': {'type': 'string'}
                }
            },
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
            401: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        },
        examples=[
            OpenApiExample(
                'Example request',
                value={
                    'username': 'testuser',
                    'password': 'testpassword123'
                },
                request_only=True
            ),
            OpenApiExample(
                'Example response',
                value={
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                    'user_id': 1,
                    'username': 'testuser'
                },
                response_only=True
            )
        ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            tokens = authenticate_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )

            if tokens:
                return Response(tokens, status=status.HTTP_200_OK)

            return Response(
                {"error": "Неверные учетные данные"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)