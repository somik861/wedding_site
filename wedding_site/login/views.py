from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import hashlib


PASSWD_HASH: bytes = b'9\xef\xc6fS\t\xec\xcb\x08\xb7\xa4@\x12,\x8d\x03\xf7zD\xdbs"Y\xe8YB\x0e7\xb6\xbaG\xf8\x99\x98x\xf8\xbb\x9d\x11\x90\xaa?\xc2\x1d\xf2\x8b\x87\x18W4ac\xee\xaf\xdc\xc6\xf4\\]YQ\xd0\x15\x86'

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