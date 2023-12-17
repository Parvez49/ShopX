import datetime

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer


class PublicResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        new_password = request.data.get("new_password")
        confirm_new_password = request.data.get("confirm_new_password")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response("Token has expired.", status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response("Invalid token.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = User.objects.get(email=payload["email"])

        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            return Response("Password has been reset successfully.")
        else:
            return Response(
                "New passwords do not match.", status=status.HTTP_400_BAD_REQUEST
            )
        

class PublicRequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.filter(email=request.data["email"]).first()
        if not user:
            raise NotFound("User with this email does not exist.")
        else:
            #send_password_reset_email.delay(request.data["email"])
            payload = {
                "email": request.data["email"],
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=1),  # Expiration after 1 hour
                "iat": datetime.datetime.utcnow(),
            }
            token = jwt.encode(payload, "secret", algorithm="HS256")
            reset_link = f"http://127.0.0.1:8000/user-auth/password/reset/{token}"
            email_subject = "Password Reset"
            message = f"Click the link below to reset your password:\n{reset_link}"
            send_mail(email_subject, message, settings.EMAIL_HOST_USER, [request.data["email"]])

            response_data = {
                "message": "Check your email to reset your password.",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({'message': 'User registered successfully'}, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email_or_phone = serializer.validated_data.get('email_or_phone')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=email_or_phone).first() \
               or User.objects.filter(phone=email_or_phone).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





