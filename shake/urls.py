from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
from auth.forms import QuizAuthenticationForm

urlpatterns = [
    # Examples:
    # url(r'^$', 'shake.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', RedirectView.as_view(pattern_name='blog:index'), name='root'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^auth/login/$', 'django.contrib.auth.views.login', {
        'authentication_form': QuizAuthenticationForm,
    }, name='login'),
    url(r'^auth/', include('django.contrib.auth.urls')),
]
