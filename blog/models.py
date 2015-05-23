# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from blog.signals import app_ready


def on_app_ready(sender, **kwargs):
    def is_follow(self, to_user):
        if self.is_authenticated() and to_user.is_authenticated():
            return self.following_set.filter(to_user=to_user).exists()
        return False
    setattr(get_user_model(), 'is_follow', is_follow)

    def follow(self, to_user):
        if not self.is_follow(to_user):
            self.following_set.create(to_user=to_user)
    setattr(get_user_model(), 'follow', follow)

    def unfollow(self, to_user):
        self.following_set.filter(to_user=to_user).delete()
    setattr(get_user_model(), 'unfollow', unfollow)

    setattr(AnonymousUser, 'is_follow', lambda *args: False)
    setattr(AnonymousUser, 'follow', lambda *args: None)
    setattr(AnonymousUser, 'unfollow', lambda *args: None)

app_ready.connect(on_app_ready)


class UserFollow(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following_set')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )


@python_2_unicode_compatible
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))

    # django gis모듈에서는 "경도,위도" 순서로 저장하므로,
    # 차후 호환성을 위해 "경도/위도" 순으로 저장토록 한다.
    lnglat = models.CharField(max_length=50, default='', verbose_name=_('lnglat'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.author.username, self.id])

    @property
    def lat(self):
        if self.lnglat:
            return self.lnglat.split(',')[1]

    @property
    def lng(self):
        if self.lnglat:
            return self.lnglat.split(',')[0]


class Comment(models.Model):
    post = models.ForeignKey(Post)
    message = models.TextField(verbose_name=_('message'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def as_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

