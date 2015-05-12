# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.views.generic import ListView
from blog.models import Post

index = ListView.as_view(model=Post, template_name='blog/index.html')
