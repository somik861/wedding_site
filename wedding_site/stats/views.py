from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
import hashlib

PASSWD_HASH: bytes = b'd\x13\x83\xda\r\xffa\x1d\x10d\xfbM\xce\xf1]\xeas"\xdf`\xc7\x95\xb2=\xa9\x9dQ\xb2f\x17!\x16\xd24j`\xa8R\xd9]2\xe7Hl\x07\xf4\xa6\x13\xa4\xa79\xd6\xf9Y\x83\x98\x9b\x95\xf7\xdf\xbb?\x00\xe6'


def check_login(f):
    def wrapper(request: HttpRequest):
        if request.session.get('login_status', 'NOK') != 'OK':
            return HttpResponseRedirect('/stats/')
        return f(request)

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
    return HttpResponse('Overview')
