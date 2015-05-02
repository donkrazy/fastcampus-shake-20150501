from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',  # noqa
    url(r'^$', 'index', name='index'),
    url(r'^(?P<id>\d+)/$', 'detail', name='post_detail'),
    url(r'^new/$', 'new', name='post_new'),
    url(r'^(?P<id>\d+)/edit/$', 'edit', name='post_edit'),
)

