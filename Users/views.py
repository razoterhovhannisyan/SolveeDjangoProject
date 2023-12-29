from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . import models
from . import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
import os
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import logging
import json

logger = logging.getLogger(__name__)

# Create your views here.

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({'message':'You are registered successfully', 'data': serializer.data},  status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'An error occurred during registration.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'message':'Logged in successfully.', 'access_token':access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





#
# class GoogleTokenCode(APIView):
#     def post(self, request):
#         CLIENT_ID = os.environ.get('CLIENT_ID')
#         CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
#         REDIRECT_URI = request.data.get('http://127.0.0.1:8000/users/google-token/')
#
#         auth_code = request.data.get('code')
#         logger.info(f"Google Authorization Code: {auth_code}")
#
#         if not auth_code:
#             logger.error('Authorization code not provided')
#             return Response({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)
#
#         data = {
#             'code': auth_code,
#             'client_id': CLIENT_ID,
#             'client_secret': CLIENT_SECRET,
#             'redirect_uri': REDIRECT_URI,
#             'grant_type': 'authorization_code'
#         }
#
#         token_exchange_endpoint = 'https://oauth2.googleapis.com/token'
#
#         try:
#             response = requests.post(token_exchange_endpoint, data=data)
#             response.raise_for_status()
#
#             tokens = response.json()
#
#             access_token = tokens.get('id_token')
#             user_profile_detailed = self.decode_google_id_token(access_token) if access_token else {}
#
#             return Response({
#                 'tokens': tokens,
#                 'user_profile_detailed': user_profile_detailed
#             }, status=status.HTTP_200_OK)
#
#         except requests.RequestException as e:
#             logger.error(f"Error in Google token exchange: {e}")
#
#             try:
#                 response_content = response.json()
#             except json.JSONDecodeError:
#                 response_content = response.content
#
#             logger.error(f"Response content: {response_content}")
#
#
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# class FacebookTokenCode(APIView):
#     def post(self, request):
#         APP_ID = os.environ.get('APP_ID')
#         APP_SECRET = os.environ.get('APP_SECRET')
#         REDIRECT_URI = request.data.get('http://127.0.0.1:8000/users/facebook-token/')
#         #https://domain.ngrok-free.app/facebook-token
#
#         auth_code = request.data.get('code')
#         logger.info(f"Facebook Authorization Code: {auth_code}")
#
#         if not auth_code:
#             logger.error('Authorization code not provided')
#             return Response({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)
#
#         token_exchange_endpoint = 'https://graph.facebook.com/v12.0/oauth/access_token'
#         exchange_params = {
#             'client_id': APP_ID,
#             'client_secret': APP_SECRET,
#             'redirect_uri': REDIRECT_URI,
#             'code': auth_code,
#         }
#
#         try:
#             response = requests.get(token_exchange_endpoint, params=exchange_params)
#             response.raise_for_status()
#             token_data = response.json()
#
#             user_info_endpoint = 'https://graph.facebook.com/v12.0/me'
#             user_info_params = {
#                 'fields': 'id,email,name',
#                 'access_token': token_data['access_token'],
#             }
#
#             user_info_response = requests.get(user_info_endpoint, params=user_info_params)
#             user_info_response.raise_for_status()
#             user_info = user_info_response.json()
#
#             return Response({
#                 'token_data': token_data,
#                 'user_info': user_info
#             }, status=status.HTTP_200_OK)
#
#         except requests.RequestException as e:
#             logger.error(f"Error in Facebook token exchange: {e}")
#
#             try:
#                 response_content = response.json()
#             except json.JSONDecodeError:
#                 response_content = response.content
#
#             logger.error(f"Response content: {response_content}")
#
#
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
