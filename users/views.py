from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .serializers import UserSerializer, CustomTokenObtainPairSerializer, OrganizerSerializer
from .authentication import CookieJWTAuthenticatation
from .models import Organizer, Guest


class UserViewSet(viewsets.ModelViewSet) :
    serializer_class = UserSerializer

class SigninView(TokenObtainPairView) :
    # serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class TokenRefreshView(TokenRefreshView) :
    permission_classes = [AllowAny]


class LoginView(APIView) :
    permission_classes = [AllowAny]

    def post(self, request) :
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user :
            return Response({'error' : 'Invalid credentials'}, status=400)
        
        refresh = RefreshToken.for_user(user)
        response = Response({"message": "Login successful"})
        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False, # True for production
            samesite="Lax",
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response
    

class RefreshTokenView(APIView) :
    def post(self, request) :
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token :
            return Response({"error": "No refresh token provided"}, status=400)
        
        try :
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"message": "Token refreshed"})
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            return response
        except Exception :
            return Response({"error": "Invalid refresh token"}, status=400)
        

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response({"detail": "Logout successful"}, status=200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
        

class ProtectedView(APIView) :
    authentication_classes = [CookieJWTAuthenticatation]
    permission_classes = [IsAuthenticated]

    def get(self, request) :
        return Response({"message": "You are authenticated!"})
    

class MeView(APIView) :
    authentication_classes = [CookieJWTAuthenticatation]
    permission_classes = [AllowAny]

    def get(self, request) :
        if not request.user or not request.user.is_authenticated :
            return Response({"error": "User not authenticated"}, status=401)
        
        return Response({
            'id': request.user.id,
            'username': request.user.username,
        }, status=200)
    

class ProfileView(viewsets.ModelViewSet) :
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthenticatation]
    
    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
    

class RegisterView(APIView) :
    permission_classes = [AllowAny]

    def post(self, request) :
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not username or not password or not confirm_password :
            return Response({ "error": "Some fields are missing" }, status=HTTP_400_BAD_REQUEST)

        if password != confirm_password :
            return Response({ "error": "Passwords do not match" }, status=HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists() :
            return Response({ "error": "Username already exists" }, status=HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        guest = Guest.objects.create(user=user)
        guest.save()
        return Response({ "message": "User created" }, status=HTTP_201_CREATED)