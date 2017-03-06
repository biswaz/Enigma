from django.utils.safestring import mark_safe
from django.conf import settings
from django.db import models

class Phase(models.Model):
    phase = models.IntegerField()
    pool_qns = models.IntegerField(default=0)
    max_qns = models.IntegerField(default=0)

    def __str__(self):
        return "Phase " + str(self.phase)


class Image(models.Model):
    image = models.ImageField(null=True)
    name = models.CharField(max_length=20)

    def image_img(self):
        return mark_safe('<img src=' + settings.MEDIA_URL + '%s width="150" height="150" />' % (self.image))

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.TextField(blank=True)
    clue = models.TextField(blank=True)
    images = models.ManyToManyField(Image, blank=True)
    answer = models.CharField(blank=False, max_length=255)
    phase = models.ForeignKey(Phase, null=True)

    original_phase = None

    def __init__(self, *args, **kwargs):
      super(Question, self).__init__(*args, **kwargs)
      self.original_phase = self.phase


    def __str__(self):
        return "Question " + str(self.pk)
