from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
import top_layout
from .models import Survey, SurveyQuestion, TextAnswer, RatingAnswer, YesNoAnswer, YesNoDcAnswer, AlcoholAnswer, Answer, Respondent, RVSP1, RVSP2, RVSP3, RVSP4
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import register
from django.utils import timezone
from login.views import check_login
from . import humans_db
from itertools import chain
from typing import Any


@register.filter
def get_form_item(dct, key):
    return dct.get(str(key), '')


class FormException(Exception):
    pass

# Create your views here.


@check_login
def index(request) -> HttpResponse:

    surveys = Survey.objects.all()

    context = {'top_layout': top_layout.get(), 'surveys': surveys}
    return render(request, 'survey/index.html', context)


@check_login
@csrf_protect
def survey(request: HttpRequest, survey_id: int) -> HttpResponse:

    prefilled = {}
    if request.method == 'POST':
        prefilled = request.POST.dict()

    # save survey
    if 'send' in prefilled:
        try:
            save_survey(request, survey_id)
            prefilled = {'form_success': 'Dotazník úspěšně odeslán'}
        except FormException as e:
            prefilled['form_error'] = str(e)

    if 'load' in prefilled:
        try:
            prefilled = load_survey(request, survey_id)
            prefilled['form_success'] = 'Dotazník úspěšně nahrán'
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

    return render(request, 'survey/survey.html', context)


def _get_latest_answer(answers):
    return max(answers, key=lambda x: x.answer_dt)


def load_survey(request: HttpRequest, survey_id: int) -> dict[str, str]:
    survey = get_object_or_404(Survey, id=survey_id)

    data = request.POST.dict()
    if not data['respondent']:
        raise FormException(
            'Pro nahrátí předchozích odpovědí musíte vyplnit své jméno')

    try:
        resp = Respondent.objects.get(full_name=data['respondent'])
    except Respondent.DoesNotExist:
        raise FormException('Zadané jméno není v databázi')

    # name; load-button; csrf-token
    if len(list(filter(lambda x: x, data.values()))) > 3:
        raise FormException(
            'Pro nahrátí předchozích smažte svůj dosavadní výběr (např.: znovu otevřete dotazník).')

    out = {'respondent': data['respondent']}
    for answer_type in [RatingAnswer, TextAnswer, YesNoAnswer, YesNoDcAnswer, AlcoholAnswer]:
        all_answers = list(filter(lambda a: a.question.survey ==
                           survey, answer_type.objects.filter(respondent=resp)))
        unique_ids = set(map(lambda x: x.id, all_answers))
        for id_ in unique_ids:
            answers_id = list(filter(lambda x: x.id == id_, all_answers))
            if len(answers_id) == 0:
                continue

            answ = _get_latest_answer(answers_id)

            value = answ.value

            if answer_type is YesNoDcAnswer:
                match value:
                    case True:
                        value = 'Yes'
                    case False:
                        value = 'No'
                    case None:
                        value = 'dc'

            if answer_type is YesNoAnswer:
                value = 'Yes' if value else 'No'

            out[str(answ.question.id)] = str(value)

    return out


def save_survey(request: HttpRequest, survey_id: int) -> None:
    survey = get_object_or_404(Survey, id=survey_id)
    questions = SurveyQuestion.objects.all().filter(survey=survey)

    data = request.POST.dict()
    if not data['respondent']:
        raise FormException('Zadejte prosím své jméno, ať víme, kdo jste :-)')

    resp, _ = Respondent.objects.get_or_create(full_name=data['respondent'])

    for question in questions:
        if not (value := data.get(str(question.id), '')):
            continue

        answ: Answer
        match question.answer_type:
            case SurveyQuestion.AnswerType.RATING:
                answ = RatingAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=timezone.now(),
                    value=int(value),
                )
            case SurveyQuestion.AnswerType.TEXT:
                answ = TextAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=timezone.now(),
                    value=value,
                )
            case SurveyQuestion.AnswerType.YES_NO:
                answ = YesNoAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=timezone.now(),
                    value=value == 'Yes',
                )
            case SurveyQuestion.AnswerType.YES_NO_DC:
                if value == 'Yes':
                    val = True
                elif value == 'No':
                    val = False
                else:
                    val = None

                answ = YesNoDcAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=timezone.now(),
                    value=val,
                )
            case SurveyQuestion.AnswerType.ALCOHOL:
                answ = RatingAnswer(
                    question=question,
                    respondent=resp,
                    answer_dt=timezone.now(),
                    value=int(value),
                )

        answ.save()


@check_login
def rsvp(request) -> HttpResponse:
    entities = sorted(chain(humans_db.RSVP_TYPE_1,
                            humans_db.RSVP_TYPE_2, humans_db.RSVP_TYPE_3, humans_db.RSVP_TYPE_4))

    context = {'top_layout': top_layout.get(), 'entities': entities}
    return render(request, 'survey/rvsp_main.html', context)


@check_login
@csrf_protect
def rvsp_quest(request, name: str) -> HttpResponse:
    context = {'top_layout': top_layout.get()}
    context['name'] = name
    if name in humans_db.RSVP_TYPE_1:
        try:
            rvsp = RVSP1.objects.get(name=name)
        except RVSP1.DoesNotExist:
            rvsp = RVSP1(name=name, participation='', journey=0)
        if request.method == 'POST':
            data = request.POST.dict()
            context['data_participation'] = data.get('participation', '')
            context['data_journey'] = data.get('journey', '')
            err = ''

            if 'participation' not in data:
                err = 'Nezapomeňte nám dát prosím vědět, zda se zúčastníte'
            else:
                part = data['participation']
                if part == 'yes' and 'journey' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, zda potřebujete něco zařídit'
            if len(err) == 0:
                rvsp.participation = data['participation'] == 'yes'
                rvsp.journey = int(data.get('journey', '0'))

                rvsp.save()
                context['form_success'] = 'Úspěšně odesláno'
            else:
                context['form_error'] = err
        else:
            context['data_participation'] = 'yes' if rvsp.participation else 'no'
            context['data_journey'] = str(rvsp.journey)

        return render(request, 'survey/rvsp_1.html', context)

    if name in humans_db.RSVP_TYPE_2:
        names = name.split('+')
        context['name1'] = names[0].strip()
        context['name2'] = names[1].strip()
        try:
            rvsp = RVSP2.objects.get(name=name)
            context['data_participation1'] = 'yes' if rvsp.participation_1st else 'no'
            context['data_participation2'] = 'yes' if rvsp.participation_2nd else 'no'
            context['data_journey'] = str(rvsp.journey)
        except RVSP2.DoesNotExist:
            rvsp = RVSP2(name=name, participation_1st=False,
                         participation_2nd=False, journey=0)
        if request.method == 'POST':
            data = request.POST.dict()
            context['data_participation1'] = data.get('participation1', '')
            context['data_participation2'] = data.get('participation2', '')
            context['data_journey'] = data.get('journey', '')
            err = ''

            if 'participation1' not in data or 'participation2' not in data:
                err = 'Nezapomeňte nám dát prosím vědět, zda se zúčastníte'
            else:
                part_atleast_1 = 'yes' in {
                    data['participation1'], data['participation2']}
                if part_atleast_1 and 'journey' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, zda potřebujete něco zařídit'
            if len(err) == 0:
                rvsp.participation_1st = data['participation1'] == 'yes'
                rvsp.participation_2nd = data['participation2'] == 'yes'
                rvsp.journey = int(data.get('journey', '0'))

                rvsp.save()
                context['form_success'] = 'Úspěšně odesláno'
            else:
                context['form_error'] = err

        return render(request, 'survey/rvsp_2.html', context)

    if name in humans_db.RSVP_TYPE_3:
        names = name.split('+')
        context['name1'] = names[0].strip()
        try:
            rvsp = RVSP3.objects.get(name=name)
            context['data_participation1'] = 'yes' if rvsp.participation_1st else 'no'
            context['data_participation2'] = 'yes' if rvsp.participation_2nd else 'no'
            context['data_2nd_name'] = rvsp.name_2nd
            context['data_journey'] = str(rvsp.journey)
        except RVSP3.DoesNotExist:
            rvsp = RVSP3(name=name, participation_1st=False,
                         participation_2nd=False, journey=0)
        if request.method == 'POST':
            data = request.POST.dict()
            context['data_participation1'] = data.get('participation1', '')
            context['data_participation2'] = data.get('participation2', '')
            context['data_2nd_name'] = data.get('2nd_name', '')
            context['data_journey'] = data.get('journey', '')
            err = ''

            if 'participation1' not in data or 'participation2' not in data:
                err = 'Nezapomeňte nám dát prosím vědět, zda se zúčastníte'
            else:
                part_atleast_1 = 'yes' in {
                    data['participation1'], data['participation2']}
                if part_atleast_1 and 'journey' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, zda potřebujete něco zařídit'

            if len(err) == 0:
                if data['participation2'] == 'yes' and data['2nd_name'] == '':
                    err = 'Nezapomeňte nám dát prosím vědět, jak se jmenuje vaše +1'

            if len(err) == 0:
                rvsp.participation_1st = data['participation1'] == 'yes'
                rvsp.participation_2nd = data['participation2'] == 'yes'
                rvsp.name_2nd = data['2nd_name']
                rvsp.journey = int(data.get('journey', '0'))

                rvsp.save()
                context['form_success'] = 'Úspěšně odesláno'
            else:
                context['form_error'] = err

        return render(request, 'survey/rvsp_3.html', context)

    if name in humans_db.RSVP_TYPE_4:
        names = name.split('+')
        context['name1'] = names[0].strip()
        context['name2'] = names[1].strip()
        try:
            rvsp = RVSP4.objects.get(name=name)
            context['data_participation1'] = 'yes' if rvsp.participation_1st else 'no'
            context['data_participation2'] = 'yes' if rvsp.participation_2nd else 'no'
            context['data_participation3'] = 'yes' if rvsp.participation_children else 'no'
            context['data_child_chair'] = str(rvsp.children_place)
            context['data_child_food'] = str(rvsp.children_food)
            context['data_journey'] = str(rvsp.journey)
        except RVSP4.DoesNotExist:
            rvsp = RVSP4(name=name)
        if request.method == 'POST':
            data = request.POST.dict()
            context['data_participation1'] = data.get('participation1', '')
            context['data_participation2'] = data.get('participation2', '')
            context['data_participation3'] = data.get('participation3', '')
            context['data_child_chair'] = data.get('child_chair', '')
            context['data_child_food'] = data.get('child_food', '')
            context['data_journey'] = data.get('journey', '')
            err = ''

            if 'participation1' not in data or 'participation2' not in data or 'participation3' not in data:
                err = 'Nezapomeňte nám dát prosím vědět, zda se (nebo vaše děti) zúčastníte'

            # at least one
            if len(err) == 0 and 'yes' in {
                    data['participation1'], data['participation2'], data['participation3']}:
                if 'journey' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, zda potřebujete něco zařídit'

            # children are coming
            if len(err) == 0 and data['participation3'] == 'yes':
                if 'child_chair' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, kde budou děti sedět'
                elif 'child_food' not in data:
                    err = 'Nezapomeňte nám dát prosím vědět, co budou děti jíst'

            if len(err) == 0:
                rvsp.participation_1st = data['participation1'] == 'yes'
                rvsp.participation_2nd = data['participation2'] == 'yes'
                rvsp.participation_children = data['participation3'] == 'yes'
                rvsp.children_place = int(data.get('child_chair', '0'))
                rvsp.children_food = int(data.get('child_food', '0'))
                rvsp.journey = int(data.get('journey', '0'))

                rvsp.save()
                context['form_success'] = 'Úspěšně odesláno'
            else:
                context['form_error'] = err

        return render(request, 'survey/rvsp_4.html', context)

    raise Http404
