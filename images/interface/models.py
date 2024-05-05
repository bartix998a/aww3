from django.db import models
import django.utils
from django.contrib.auth.models import User

import datetime

import django.utils.timesince
import django.utils.timezone

class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)
    def __str__(self) -> str:
        return str(self.title)

class Image(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sizex = models.IntegerField()
    sizey = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication_date = models.DateTimeField(null=False, default=django.utils.timezone.now)
    description = models.CharField(null=True, max_length=1000)
    tags = models.ManyToManyField(Tag)
    def __str__(self) -> str:
        return self.title

class Rect(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    sizex = models.IntegerField()
    sizey = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=200, default='white')
    def __str__(self) -> str:
        return str(self.id)
