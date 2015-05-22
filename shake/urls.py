# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    # Examples:
    # url(r'^$', 'shake.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(pattern_name='blog:index'), name='root'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),

    # django-allauth 의 logout 뷰에서는 이메일변경 기능이 있는데,
    # 일단 이 기능을 노출하지 않기 위해서 적용.
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),
]
