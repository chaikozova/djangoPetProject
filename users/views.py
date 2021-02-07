from datetime import datetime, timedelta
from random import randint

from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, ConfirmationCode


class RegisterApiView(APIView):
    def send_sms(self, subject, message, recipient_list):
        return f'{subject}, {message}, {recipient_list}'

    def post(self, request):
        phonenumber = request.data.get('phonenumber')  # +996700012122
        user = User.objects.create_user(phonenumber=phonenumber,
                                        is_active=False)
        user.save()
        code = randint(1000, 9999)  # 1111
        confirmation_code = ConfirmationCode()
        confirmation_code.code = str(code)
        confirmation_code.user = user
        confirmation_code.valid_until = datetime.now() + timedelta(minutes=20)
        confirmation_code.save()
        self.send_sms(subject='Code confirmation',
                  message=f'http://127.0.0.1:8000/confirm/{code}',
                  recipient_list=[phonenumber])
        # sms_send()
        print(code)
        return Response(status=status.HTTP_200_OK)