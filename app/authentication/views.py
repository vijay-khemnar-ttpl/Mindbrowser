# Django Imports
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Rest Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authentication.models import Profile
from django.contrib.auth.models import User
from authentication.serializers import UserSerializer
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

# Other Imports
from .serializers import ProfileSerializer, UserSerializer

# simple JWT Imports
from authentication.serializers import UserSerializer, CustomTokenObtainPairSerializer


# file imports


# Register User
class HandleRegister(APIView):

    @csrf_exempt
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            email = User.objects.all().values_list('email', flat=True)
            if request.data.get('email') in email:
                return Response(data = {'email': "email Already Exists"}, status = status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                user = serializer.save()
                if user:
                    token = RefreshToken.for_user(user)
                    user_data = serializer.data
                    return Response({"username": user_data['username'], "token": str(token.access_token)},
                                    status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            print(e)
            return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Logout User
class HandleLogout(APIView):
    permission_classes = [IsAuthenticated, ]

    @csrf_exempt
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({"success": "Logged Out Successfully!"}, status=status.HTTP_200_OK)


class HandleHomePage(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        return Response({"IsAuthenticated": request.user.is_authenticated})


@method_decorator(name='put', decorator=csrf_exempt)
class UpdateProfileView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserDetailsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    lookup_field = "id"
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(id=self.kwargs["id"])
