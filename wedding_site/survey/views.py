from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import top_layout
from .models import Survey, SurveyQuestion, TextAnswer, RatingAnswer, YesNoAnswer, YesNoDcAnswer, Answer, Respondent
from django.views.decorators.csrf import csrf_protect
from django.template.defaulttags import register
from django.utils import timezone


@register.filter
def get_form_item(dct, key):
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
    if 'send' in prefilled:
        try:
            save_survey(request, survey_id)
            return HttpResponseRedirect('/survey')
        except FormException as e:
            prefilled['form_error'] = str(e)

    if 'load' in prefilled:
        try:
            prefilled = load_survey(request, survey_id)
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
        raise FormException('Pro nahrátí předchozích odpovědí musíte vyplnit své jméno')
    
    try:
        resp = Respondent.objects.get(full_name=data['respondent'])
    except Respondent.DoesNotExist:
        raise FormException('Zadané jméno není v databázi')
    

    # name; load-button; csrf-token
    if len(list(filter(lambda x: x, data.values()))) > 3:
        raise FormException('Pro nahrátí předchozích smažte svůj dosavadní výběr (např.: znovu otevřete dotazník).')
    
    out = {'respondent' : data['respondent']}
    for answer_type in [RatingAnswer, TextAnswer, YesNoAnswer, YesNoDcAnswer]:
        answ = _get_latest_answer(
            filter(lambda a:a.question.survey == survey , answer_type.objects.filter(respondent=resp))
        )
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

        answ.save()
