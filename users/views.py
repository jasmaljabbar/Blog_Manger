from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta,datetime
from django.middleware import csrf
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate



from . import serializers
from .models import Profile
# Create your views here.


User = get_user_model()


class UserRegisterationAPIView(GenericAPIView):
    """
    An endpoint for the client to create a new User.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegisterationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    return Response({
        'isAuthenticated': True,
        'user': {
            'id': request.user.id,
            'email': request.user.email,
        }
    })



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



class UserLoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        
        if user is not None and user.is_active:
            data = get_tokens_for_user(user)
            
            response = Response({
                "status": "success",
                "user": {
                    "id": user.id,
                    "email": user.email,
                }
            })
            
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'], 
                value=data["access"],
                httponly=True,
                samesite='Lax',  # Try this instead of settings value
                secure=False,    # Set to True in production with HTTPS
                max_age=3600,
                path='/'        # Make sure path is set
            )
            
            # Also set refresh token
            response.set_cookie(
                key='refresh_token',
                value=data["refresh"],
                httponly=True,
                samesite='Lax',
                secure=False,    # Set to True in production with HTTPS
                max_age=3600 * 24 * 14,  # 14 days
                path='/'
            )
            
            return response
        else:
            return Response(
                {"error": "Invalid username or password!"},
                status=status.HTTP_404_NOT_FOUND
            )


    

class UserLogoutAPIView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        response = Response({"message": "Logged out successfully"})
        
        # Delete cookies
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    
class TokenRefreshView(GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response(
                {"error": "Refresh token not found"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            response = Response({
                "success": True,
                "message": "Token refreshed successfully"
            })

            response.set_cookie(
                'access_token',
                str(access_token),
                max_age=300,  # 5 minutes
                httponly=True,
                secure=settings.COOKIE_SECURE,
                samesite=settings.COOKIE_SAMESITE
            )

            return response

        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        
class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user

class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile

class UserAvatarAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user avatar
    """

    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileAvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile