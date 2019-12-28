# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from enigma.oth.models import Question, Phase


def get_or_create_phase():
    phase, created = Phase.objects.get_or_create(phase=1)
    return phase


class User(AbstractUser):

    phone = models.CharField(_('Phone number'), max_length=10)
    college = models.CharField(_('Name of your college'), max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    date_last_ans = models.DateTimeField(null=True)
    cur_phase = models.ForeignKey(Phase, null=True, on_delete=models.PROTECT, default=get_or_create_phase)
    completed_qns = models.ManyToManyField(Question, related_name="compq_related", blank=True)
    cur_qn = models.ForeignKey(Question, null=True, blank=True, related_name="curq_related", on_delete=models.SET_NULL)

    #    def get_time_taken(self):
    #        if (self.date_last_ans == None):
    #            return None
    #        else:
    #            delta = self.date_last_ans
    #            return round(delta.days,2), round(delta.seconds/3600, 2), round((delta.seconds/60)%60, 2)

    def level(self):
        return self.completed_qns.count()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
