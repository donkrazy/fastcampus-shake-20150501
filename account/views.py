# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'blog/form.html'
    success_url = reverse_lazy('root')

    def form_valid(self, form):
        response = super(SignupView, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        auth_login(self.request, user)
        messages.info(self.request, '가입되셨습니다. 환영합니다.')
        return response

