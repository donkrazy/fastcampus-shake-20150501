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
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', name='jsi18n'),
]
