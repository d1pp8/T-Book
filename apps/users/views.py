from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.throttling import UserRateThrottle

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    LoginSerializer,
    LoginResponseSerializer
)

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)

import logging
logger = logging.getLogger(__name__)


class LoginThrottle(UserRateThrottle):
    rate = "5/min"

@extend_schema(
    tags=['Authentication'],
    summary="Sign up",
    description="Creates a new user account.",
    request=UserRegistrationSerializer,
    responses=UserSerializer
)
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


@extend_schema(
    tags=['Authentication'],
    summary="Sign in",
    description="Only registered users can sign in.",
    request=LoginSerializer,
    responses=LoginResponseSerializer

)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [LoginThrottle]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })


@extend_schema(
    tags=['Authentication'],
    summary="Refresh access token",
    description="Returns a new access token using a valid refresh token.",
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


@extend_schema_view(
    get=extend_schema(
        tags=["Users"],
        summary="User profile",
        description="Returns the authenticated user's profile.",
        responses=UserSerializer,
    ),
    patch=extend_schema(
        tags=["Users"],
        summary="Update profile",
        description="Updates the authenticated user's profile.",
        request=UserUpdateSerializer,
        responses=UserSerializer,
    ),
    put=extend_schema(
        tags=["Users"],
        summary="Replace profile",
        request=UserUpdateSerializer,
        responses=UserSerializer,
    ),
)
class ProfileView(generics.RetrieveUpdateAPIView):
    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserUpdateSerializer


@extend_schema(
    tags=['Users'],
    summary="Change password",
    description=
    """
    Changes the authenticated user's password.

    Requirements:
    
    - Current password must be provided.
    - New password must be different from the current password.
    """,
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(
            description="Password updated successfully"
        ),
        400: OpenApiResponse(
            description="Validation error or wrong password"
        )
    }
)

class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'error': 'Wrong password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response(
                {'message': 'Password updated successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )