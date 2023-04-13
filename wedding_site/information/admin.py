from django.contrib import admin

from .models import InfoBlock, Information

# Register your models here.

for elem in [InfoBlock, Information]:
    admin.site.register(elem)
