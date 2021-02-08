from datetime import datetime, timedelta
from random import randint

from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, ConfirmationCode


class RegisterApiView(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')  # +996700012122
        password = request.data.get('password')
        user = User.objects.create_user(username=phone,
                                        password=password, is_active=False)
        user.save()
        code = randint(1000, 9999)  # 1111
        confirmation_code = ConfirmationCode()
        confirmation_code.code = str(code)
        confirmation_code.user = user
        confirmation_code.valid_until = datetime.now() + timedelta(minutes=20)
        confirmation_code.save()
        print('code:', code)
        return Response(status=status.HTTP_200_OK)


class ConfirmApiView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get('code')
        codes = ConfirmationCode.objects.get(code=code,
                                             valid_until__gte=datetime.now())
        user = codes.user
        user.is_active = True
        user.save()
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        codes.delete()
        return Response(data={'token': token.key},
                        status=status.HTTP_200_OK)


class LoginApiView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'],
                            code=request.data.get('code', 'admin123'))
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User not found'})
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)