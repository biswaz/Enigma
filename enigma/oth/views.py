from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django import forms
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone
from .models import Question, Phase
from enigma.users.models import User

import random

def pick_random_qn(completed_qns, phase):
    #TODO: test this
    picked_qns = Question.objects.filter(phase=phase).exclude(pk__in=completed_qns.all())
    rand_qn = random.choice(picked_qns)
    return rand_qn


class AnswerForm(forms.Form):
    answer = forms.CharField(label='Crack the code')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AnswerForm, self).__init__(*args, **kwargs)

    def clean_answer(self):
        answer = self.cleaned_data['answer']
        if answer != self.request.user.cur_qn.answer.replace(" ", "").lower():
            raise forms.ValidationError("Incorrect answer")
        return answer


class PlayView(FormMixin, DetailView):

    template_name = 'oth/play.html'
    form_class = AnswerForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        cur_phase = user.cur_phase
        last_phase = Phase.objects.all().order_by('-phase').first()
        ans_qn_count = user.completed_qns.filter(phase=cur_phase).count()

        if cur_phase == last_phase and ans_qn_count == cur_phase.max_qns:
         return redirect('finish')
        else:
         return super(PlayView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super(PlayView, self).get_form_kwargs()
        kw['request'] = self.request # the trick!
        return kw

    def get_success_url(self):
        return reverse('play_view')

    def get_context_data(self, **kwargs):
        context = super(PlayView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_invalid(self, form):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)



    def form_valid(self, form):
        user = self.request.user
        user.completed_qns.add(user.cur_qn)
        user.save()

        completed_qns = user.completed_qns
        cur_phase = user.cur_phase

        ans_qn_count = completed_qns.filter(phase=cur_phase).count()
        last_phase = Phase.objects.all().order_by('-phase').first()

        #upgrade phase, except at last_phase
        if(ans_qn_count == cur_phase.max_qns and cur_phase != last_phase):
            next_phase = Phase.objects.get(phase=cur_phase.phase + 1)
            user.cur_phase = next_phase
            user.save()

        cur_qn = pick_random_qn(user.completed_qns, user.cur_phase)
        cur_qn_id = cur_qn.pk
        user.cur_qn = cur_qn

        user.date_last_ans = timezone.now()
        user.save()
        return super(PlayView, self).form_valid(form)


    def get_object(self):
        try:
            cur_qn_id = self.request.user.cur_qn.pk

        #AttributeError when qn doesnt exist
        except AttributeError:
            completed_qns = self.request.user.completed_qns
            phase = self.request.user.cur_phase
            user = self.request.user

            cur_qn = pick_random_qn(completed_qns, phase)
            cur_qn_id = cur_qn.pk

            user.cur_qn = cur_qn
            user.save()
        return get_object_or_404(Question, pk=cur_qn_id)

    def post(self, request, *args, **kwargs):
        self.object = None
        #TODO: remove auth check and  implement loginrequiredmixin?
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        #form = AnswerForm(request.POST, request=request)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class FinishView(TemplateView):
    template_name = 'oth/finish.html'

class LeaderBoardView(ListView):

    queryset = User.objects.annotate(level=Count('completed_qns')).order_by('-level', 'date_last_ans')
    template_name = 'users/leaderboard.html'
