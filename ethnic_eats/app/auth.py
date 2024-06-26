from .serializers import UserLoginSerielizer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView


from rest_framework import permissions, viewsets, status
from .serializers import GroupSerializer, UserInfoSerializer, UserLoginSerielizer, CreateNewUserSerializer, ChangePassWordSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django.core.mail import send_mail

from django.contrib.auth.models import Group, User

class Register(APIView):
    def post(self, request):
        data = request.data
        role = data.get('role')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a new user if username and email are unique
        user_data = {}
        user_data['username'] = username
        user_data['email'] = email
        user_data['password'] = password
        serialized_user_data = CreateNewUserSerializer(data = user_data, many = False)
        if serialized_user_data.is_valid():
            user = User.objects.create_user(username=username, email=email, password=password)
            if role == "Cuisine Owner":
                cuisine_owner_group, created = Group.objects.get_or_create(name='Cuisine Owner')
                user.groups.add(cuisine_owner_group)
            subject = "Account creation successful"
            message = "You have successfully created an acount with Ethnic Eats"
            sender_email = "tituskennedy74@gmail.com"
            recipient_list = [user.email]
            send_mail(subject, message, sender_email, recipient_list, fail_silently=False,
                      )
            user_data = User.objects.filter(email = email).first()
            user_info_serializer = UserInfoSerializer(user_data)
            return JsonResponse(data = user_info_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized_user_data.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserLoginSerielizer(data=data)
        if serializer.is_valid():
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access = AccessToken.for_user(user)
                user_data = {
                    "email": user.email,
                    "username": user.username,
                    "access": str(access),
                    "refresh": str(refresh)
                }
                return JsonResponse(user_data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return JsonResponse({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return JsonResponse({"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_info = User.objects.filter(id = user.id).first()
        if user_info:
            user_serializer = UserInfoSerializer(user_info)
            return JsonResponse(data = user_serializer.data, status = status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Bad Request"}, status = status.HTTP_400_BAD_REQUEST)




            
        

