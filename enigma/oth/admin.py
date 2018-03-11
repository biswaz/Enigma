from django.contrib import admin

from .models import Question, Image, Phase

admin.site.register(Question)
admin.site.register(Phase)
