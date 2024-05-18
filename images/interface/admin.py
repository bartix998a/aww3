from django.contrib import admin
from .models import Image, Rect, Tag
# Register your models here.

admin.site.register(Image)
admin.site.register(Rect)
admin.site.register(Tag)