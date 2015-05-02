from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',  # noqa
    url(r'^$', 'index', name='index'),
)

