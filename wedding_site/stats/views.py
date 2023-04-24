from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from survey.models import Respondent, Survey, TextAnswer, RatingAnswer,  YesNoAnswer, YesNoDcAnswer, SurveyQuestion, Answer
from typing import Any
from itertools import chain
from django.template.defaulttags import register
import hashlib


@register.filter
def get_item(dct, key):
    return dct[key]


PASSWD_HASH: bytes = b'd\x13\x83\xda\r\xffa\x1d\x10d\xfbM\xce\xf1]\xeas"\xdf`\xc7\x95\xb2=\xa9\x9dQ\xb2f\x17!\x16\xd24j`\xa8R\xd9]2\xe7Hl\x07\xf4\xa6\x13\xa4\xa79\xd6\xf9Y\x83\x98\x9b\x95\xf7\xdf\xbb?\x00\xe6'
ANSWERS = [TextAnswer, RatingAnswer, YesNoAnswer, YesNoDcAnswer]


def check_login(f):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.session.get('login_status', 'NOK') != 'OK':
            return HttpResponseRedirect('/stats/')
        return f(request, *args, **kwargs)

    return wrapper

# Create your views here.


@csrf_protect
def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        data = request.POST.dict()
        if 'login' in data:
            passwd = data['passwd']
            if hashlib.sha512(passwd.encode(encoding='utf-8')).digest() == PASSWD_HASH:
                request.session['login_status'] = 'OK'

    if request.session.get('login_status', 'NOK') == 'OK':
        return HttpResponseRedirect('/stats/main_view')

    return render(request, 'stats/login.html', {})


@check_login
def main_view(request: HttpRequest) -> HttpResponse:
    context: dict[str, Any] = {}
    context['respondents'] = Respondent.objects.all()
    context['surveys'] = Survey.objects.all()

    return render(request, 'stats/main_view.html', context)


@check_login
def respondent_view(request: HttpRequest, resp_id: int, verbose: bool = False) -> HttpResponse:
    respondent = get_object_or_404(Respondent, id=resp_id)

    answers = list(chain(*(x.objects.filter(respondent=respondent)
                    for x in ANSWERS)))
    
    question_ids = set(answ.question.id for answ in answers)

    questions = list(chain(*(SurveyQuestion.objects.filter(id=id_)
                      for id_ in question_ids)))
    survey_ids = set(quest.survey.id for quest in questions)

    surveys = list(chain(*(Survey.objects.filter(id=id_) for id_ in survey_ids)))

    question_dct: dict[int, list[SurveyQuestion]] = {}
    for survey_id in survey_ids:
        question_dct[survey_id] = list(
            filter(lambda x: x.survey.id == survey_id,  questions))

    answer_dct: dict[int, list[Answer]] = {}
    for question_id in question_ids:
        answs = list(filter(lambda x: x.question.id == question_id, answers))
        if not verbose:
            answer_dct[question_id] = [max(answs, key=lambda x: x.answer_dt)]
        else:
            answer_dct[question_id] = sorted(answs, key=lambda x: x.answer_dt)

    context: dict[str, Any] = {
        'surveys': list(surveys),
        'questions': question_dct,
        'answers': answer_dct,
        'respondent': respondent
    }

    return render(request, 'stats/respondent.html', context)


@check_login
def survey_view(request: HttpRequest, survey_id: int, verbose: bool = False) -> HttpResponse:
    return HttpResponse(f'Survey view, {survey_id = }')
