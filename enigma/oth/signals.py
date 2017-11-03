from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from .models import Question, Phase

#TODO: Prevent pool_ans incrementation on qn updation
@receiver(post_save, sender=Question)
def question_save(sender, instance, **kwargs):
    qn_phase = instance.phase

    if kwargs['created']:
        qn_phase.pool_qns += 1
        qn_phase.save()
    else:
        instance.original_phase.pool_qns -= 1
        instance.phase.pool_qns += 1
        instance.original_phase.save()
        instance.phase.save()

        instance.original_phase = instance.phase
        #TODO: instance.save() ?

@receiver(post_delete, sender=Question)
def question_delete(sender, instance, **kwargs):
    qn_phase = instance.phase
    qn_phase.pool_qns -= 1
    qn_phase.save()

#TODO:set max_qns also
