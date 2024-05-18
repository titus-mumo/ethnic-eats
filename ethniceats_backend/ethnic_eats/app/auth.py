from .serializers import UserLoginSerielizer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from .serializers import GroupSerializer, UserLoginSerielizer, CreateNewUserSerializer, ChangePassWordSerializer
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from django.core.mail import send_mail


class Register(APIView):
    def post(self, request):
        data = request.data
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
            # subject = "Account creation successful"
            # message = "You have successfully crreated an acount with Ethnic Eats"
            # sender_email = "tituskennedy74@gmail.com"
            # recipient_list = [user.email]
            # send_mail(subject, message, sender_email, recipient_list
            #           )
            return JsonResponse({'message': 'Accont created successfully successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serialized_user_data.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        print(data)
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
            return JsonResponse(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if User.objects.filter(id = user.id).exists():
            data = request.data
            email = user.email
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            if not user.check_password(old_password):
                return JsonResponse({"error": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
            if old_password == new_password:
                return JsonResponse({"error": "New Password can't be the same as old password"}, status=status.HTTP_400_BAD_REQUEST)
            change_password_data = {}
            change_password_data['email'] = email
            change_password_data['old_password'] = old_password
            change_password_data['new_password'] = new_password
            serialized_data = ChangePassWordSerializer(data = change_password_data)
            if serialized_data.is_valid():
                user.set_password(new_password)
                user.save()
                return JsonResponse({"message": "Password changed successfully"}, status = status.HTTP_400_BAD_REQUEST)
            return JsonResponse(serialized_data.errors, status = status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"message": "Unauthorized Request"}, status = status.HTTP_401_UNAUTHORIZED)





            
        

