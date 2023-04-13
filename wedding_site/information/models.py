from django.db import models
from django.db.models import CharField, TextField, ForeignKey, Model

# Create your models here.


class InfoBlock(Model):
    block_name: CharField = CharField(max_length=255)


class Information(Model):
    block: ForeignKey = ForeignKey(InfoBlock, on_delete=models.CASCADE)
    title: CharField = CharField(max_length=255)
    text: TextField = TextField()
