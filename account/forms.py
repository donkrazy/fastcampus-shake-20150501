# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator


class QuizAuthenticationForm(AuthenticationForm):
    answer = forms.CharField(label='3 + 3 = ?',
                             validators=[RegexValidator(r'\d+')],
                             help_text='로그인할려면 답을 맞춰보세요.')

    def clean_answer(self):
        if int(self.cleaned_data['answer']) != 6:
            raise forms.ValidationError('땡~~~!!!')

