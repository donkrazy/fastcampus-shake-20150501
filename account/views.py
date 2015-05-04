# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog/form.html'
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        messages.info(self.request, '가입되었습니다. 로그인해주세요.')
        return super(SignupView, self).form_valid(form)

