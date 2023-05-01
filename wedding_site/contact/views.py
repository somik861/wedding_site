from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import top_layout
from django.views.decorators.csrf import csrf_protect
from typing import Any
from django.core.mail import send_mail
from login.views import check_login

# Create your views here.

@check_login
@csrf_protect
def index(request: HttpRequest) -> HttpResponse:
    context: dict[Any, Any] = {'top_layout': top_layout.get()}
    if request.method == 'POST':
        prefilled = request.POST.dict()
        context['prefilled'] = prefilled
        if not prefilled['subject']:
            err = context.get('error', '')
            err += 'Vyplňte prosím předmět.<br>'
            context['error'] = err

        if len(prefilled['message']) < 5:
            err = context.get('error', '')
            err += 'Vyplňte prosím text.<br>'
            context['error'] = err

        if 'error' not in context:
            send_mail(
                prefilled['subject'] + (f' --email: {prefilled["email"]}' if prefilled['email'] else ''),
                prefilled['message'],
                from_email=None,
                recipient_list=['jjnk.svatba@seznam.cz'],
                fail_silently=False,
            )
            context.pop('prefilled')
            context['success'] = 'Email byl úspěšně odeslán.'

    

    return render(request, 'contact/index.html', context)
