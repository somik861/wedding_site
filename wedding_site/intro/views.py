from django.shortcuts import render
from django.http import HttpResponse
import top_layout

# Create your views here.

def index(request) -> HttpResponse:
    return render(request, 'intro/index.html', {'top_layout': top_layout.get()})