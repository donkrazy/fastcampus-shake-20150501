from django.conf.urls import include, url
from accounts.forms import QuizAuthenticationForm
from accounts.views import SignupView

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^login/$', 'django.contrib.auth.views.login', {
        'authentication_form': QuizAuthenticationForm,
    }, name='login'),
    url(r'', include('django.contrib.auth.urls')),
]

