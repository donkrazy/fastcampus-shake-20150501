from django.conf.urls import patterns, url

username_pattern = r'(?P<username>[a-zA-Z0-9_]+)'

urlpatterns = patterns('blog.views_cbv',  # noqa
    url(r'^$', 'index', name='index'),
    url('^' + username_pattern + r'/(?P<pk>\d+)/$', 'detail', name='post_detail'),
    url(r'^new/$', 'new', name='post_new'),
    url(r'^(?P<pk>\d+)/edit/$', 'edit', name='post_edit'),
    url(r'^(?P<pk>\d+)/delete/$', 'delete', name='post_delete'),
    url(r'^(?P<post_id>\d+)/comments/new/$', 'comment_new', name='comment_new'),
    url(r'^(?P<post_id>\d+)/comments/(?P<pk>\d+)/edit/$', 'comment_edit',
        name='comment_edit'),
    url(r'^(?P<post_id>\d+)/comments/(?P<pk>\d+)/delete/$', 'comment_delete',
        name='comment_delete'),
    url('^' + username_pattern + '/$', 'author_home', name='author_home'),
    url('^' + username_pattern + '/follow/$', 'follow', name='author_follow'),
    url('^' + username_pattern + '/unfollow/$', 'unfollow', name='author_unfollow'),
)

urlpatterns += patterns('blog.views',  # noqa
)
