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


class RVSP1(Model):
    name: CharField = CharField(max_length=255)
    participation: BooleanField = BooleanField(null=False)
    # 1: Hotel, 2: Taxi, 3: On their own
    journey: IntegerField = IntegerField()


class RVSP2(Model):
    name: CharField = CharField(max_length=255)
    participation_1st: BooleanField = BooleanField(null=False)
    participation_2nd: BooleanField = BooleanField(null=False)
    # 1: Hotel, 2: Taxi, 3: On their own
    journey: IntegerField = IntegerField()


class RVSP3(Model):
    name: CharField = CharField(max_length=255)
    name_2nd: CharField = CharField(max_length=255)
    participation_1st: BooleanField = BooleanField(null=False)
    participation_2nd: BooleanField = BooleanField(null=False)
    # 1: Hotel, 2: Taxi, 3: On their own
    journey: IntegerField = IntegerField()


class RVSP4(Model):
    name: CharField = CharField(max_length=255)
    participation_1st: BooleanField = BooleanField(null=False)
    participation_2nd: BooleanField = BooleanField(null=False)
    participation_children: BooleanField = BooleanField(null=False)
    # 1: Chair, 2: Child chair, 3: No chair
    children_place: IntegerField = IntegerField()
    # 1: Normal, 2: Child, 3: None
    children_food: IntegerField = IntegerField()
    # 1: Hotel, 2: Taxi, 3: On their own
    journey: IntegerField = IntegerField()
