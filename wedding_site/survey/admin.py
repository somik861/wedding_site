from django.contrib import admin
from .models import *

# Register your models here.


for elem in [
    Survey,
    SurveyQuestion,
    Respondent,
    TextAnswer,
    RatingAnswer,
    YesNoAnswer,
    YesNoDcAnswer,
    AlcoholAnswer,
]:
    admin.site.register(elem)
