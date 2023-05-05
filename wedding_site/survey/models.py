from django.db import models
from django.db.models import Model, CharField, ForeignKey, TextField, IntegerField, DateTimeField, TextChoices, BooleanField

# Create your models here.


class Survey(Model):
    name: CharField = CharField(max_length=255)


class SurveyQuestion(Model):
    survey: ForeignKey = ForeignKey(Survey, on_delete=models.CASCADE)
    text: TextField = TextField()

    class AnswerType(TextChoices):
        RATING = 'rating', 'rating 1 - 5'
        TEXT = 'text'
        YES_NO = 'yes_no', 'yes - no'
        YES_NO_DC = 'yes_no_dc', 'yes, no, don\'t care'
        ALCOHOL = 'alcohol'

    answer_type: CharField = CharField(
        max_length=200,
        choices=AnswerType.choices,
        default=AnswerType.TEXT
    )


class Respondent(Model):
    full_name: CharField = CharField(max_length=255)


class Answer(Model):
    question: ForeignKey = ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    respondent: ForeignKey = ForeignKey(Respondent, on_delete=models.CASCADE)
    answer_dt: DateTimeField = DateTimeField()


class TextAnswer(Answer):
    value: TextField = TextField()


class RatingAnswer(Answer):
    value: IntegerField = IntegerField()


class YesNoAnswer(Answer):
    value: BooleanField = BooleanField()

class YesNoDcAnswer(Answer):
    value: BooleanField = BooleanField(null=True)

class AlcoholAnswer(Answer):
    value: IntegerField = IntegerField()