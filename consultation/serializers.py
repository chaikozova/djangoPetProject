from rest_framework import serializers

from consultation.models import UserQuestions, AdminAnswers


class QuestionsSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = UserQuestions
        fields = 'id text answers'.split()

    def get_answers(self, obj):
        answers = AdminAnswers.objects.filter(question=obj)
        return AnswersSerializer(answers, many=True).data


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAnswers
        fields = ('id text').split()