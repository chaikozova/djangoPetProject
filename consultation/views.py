from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from consultation.models import UserQuestions
from consultation.serializers import QuestionsSerializer


class QuestionAPIView(APIView):
    allowed_methods = ['get', 'post']
    serializer_class = QuestionsSerializer

    def get(self, request):
        questions = UserQuestions.objects.all()
        return Response(data=self.serializer_class(questions, many=True).data)

    def post(self, request):
        text = request.data.get('text')
        question = UserQuestions.objects.create(text=text)
        question.save()
        return Response(data=self.serializer_class(question).data,
                        status=status.HTTP_201_CREATED)