from django.shortcuts import render
from django.http import HttpResponse
import top_layout
from login.views import check_login

# Create your views here.
@check_login
def index(request) -> HttpResponse:
    return render(request, 'intro/index.html', {'top_layout': top_layout.get()})