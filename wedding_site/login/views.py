from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import hashlib


PASSWD_HASH: bytes = b'\xf2\xe7\xefh\xa0\x94c,R\x04\x1c\x86F\xbb\x1f/\xc0x+\x9a^\xad\xd1Mp\xcd4wW\xc1\xc8\x93o\xf4K\x83\xe7`\x13\xd7\xa3[\x01\x07\x0b<\xbc\x97\xa3\xde\xe6<\x1a\xed\xb7N\xb6\xa4s`Zl\xc2o'

def check_login(f):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.session.get('login_status', 'NOK') != 'OK':
            return HttpResponseRedirect('/')
        return f(request, *args, **kwargs)

    return wrapper

# Create your views here.

def index(request) -> HttpResponse:
    if request.method == 'POST':
        data = request.POST.dict()
        if 'login' in data:
            passwd = data['passwd']
            if hashlib.sha512(passwd.encode(encoding='utf-8')).digest() == PASSWD_HASH:
                request.session['login_status'] = 'OK'

    if request.session.get('login_status', 'NOK') == 'OK':
        return HttpResponseRedirect('/intro')

    return render(request, 'login/index.html', {})