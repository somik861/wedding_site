from django.shortcuts import render
from django.http import HttpResponse
from .models import InfoBlock, Information


# Create your views here.
def index(request) -> HttpResponse:
    out = ''
    blocks = InfoBlock.objects.all()
    for block in blocks:
        out += f'<h1>{block.block_name}</h1><br>'

    return HttpResponse(out)
