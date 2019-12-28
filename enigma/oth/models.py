from django.db import models


class Phase(models.Model):
    phase = models.IntegerField()
    pool_qns = models.IntegerField(default=0)
    max_qns = models.IntegerField(default=0)

    def __str__(self):
        return "Phase " + str(self.phase)


class Question(models.Model):
    content = models.TextField(blank=True)
    clue = models.TextField(blank=True)
    image = models.URLField(blank=True)
    answer = models.CharField(blank=False, max_length=255)
    phase = models.ForeignKey(Phase, null=True, on_delete=models.PROTECT)

    original_phase = None

    def __init__(self, *args, **kwargs):
        super(Question, self).__init__(*args, **kwargs)
        self.original_phase = self.phase

    def __str__(self):
        return "Question " + str(self.pk)
