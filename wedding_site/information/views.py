from django.shortcuts import render
from django.http import HttpResponse
from .models import InfoBlock, Information
import top_layout


# Create your views here.
def index(request) -> HttpResponse:
    blocks = InfoBlock.objects.all()
    infos: dict[InfoBlock, list[Information]] = {}

    for block in blocks:
        infos[block] = []
        infos[block].extend(Information.objects.filter(block=block))

    # return HttpResponse(out)
    context = {'infos': infos, 'top_layout': top_layout.get()}
    return render(request, 'information/index.html', context)
