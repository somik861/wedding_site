from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import top_layout
from .models import Survey, SurveyQuestion, TextAnswer, RatingAnswer, YesNoAnswer, YesNoDcAnswer, Answer, Respondent
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import register
from datetime import datetime


@register.filter
def get_item(dct, key):
    return dct.get(str(key), '')


class FormException(Exception):
    pass

# Create your views here.


def index(request) -> HttpResponse:

    surveys = Survey.objects.all()

    context = {'top_layout': top_layout.get(), 'surveys': surveys}
    return render(request, 'survey/index.html', context)


@csrf_protect
def survey(request: HttpRequest, survey_id: int) -> HttpResponse:

    prefilled = {}
    if request.method == 'POST':
        prefilled = request.POST.dict()

    # save survey
    if 'submit' in prefilled:
        try:
            save_survey(request, survey_id)
            return HttpResponseRedirect('/survey')
        except FormException as e:
            prefilled['form_error'] = str(e)

    survey = get_object_or_404(Survey, id=survey_id)
    questions = SurveyQuestion.objects.all().filter(survey=survey)

    context = {
        'top_layout': top_layout.get(),
        'survey': survey,
        'questions': questions,
        'possible_rates': list(map(lambda x: str(x), range(1, 6))),
        'prefilled': prefilled,
    }

    print(prefilled)

    return render(request, 'survey/survey.html', context)


def load_survey(request: HttpRequest, survey_id: int, respondent: str) -> HttpResponse:
    return HttpResponse('WIP: survey loading')


def save_survey(request: HttpRequest, survey_id: int) -> None:
    survey = get_object_or_404(Survey, id=survey_id)
    questions = SurveyQuestion.objects.all().filter(survey=survey)

    data = request.POST.dict()
    if not data['respondent']:
        raise FormException('Zadejte prosím své jméno, ať víme, kdo jste :-)')

    resp,_ = Respondent.objects.get_or_create(full_name=data['respondent'])

    for question in questions:
        if not (value := data.get(str(question.id), '')):
            continue

        answ: Answer
        match question.answer_type:
            case SurveyQuestion.AnswerType.RATING:
                answ = RatingAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=datetime.now(),
                    value=int(value),
                )
            case SurveyQuestion.AnswerType.TEXT:
                answ = TextAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=datetime.now(),
                    value=value,
                )
            case SurveyQuestion.AnswerType.YES_NO:
                answ = YesNoAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=datetime.now(),
                    value=value == 'Yes',
                )
            case SurveyQuestion.AnswerType.YES_NO_DC:
                if value == 'Yes':
                    val = True
                elif value == 'No':
                    val = False
                else:
                    val = None

                answ = YesNoAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=datetime.now(),
                    value=val,
                )

        answ.save()
