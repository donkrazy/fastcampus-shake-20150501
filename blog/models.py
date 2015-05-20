# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from blog.signals import app_ready


def author_is_follow(from_user, to_user):
    if from_user.is_authenticated() and to_user.is_authenticated():
        return from_user.following_set.filter(to_user=to_user).exists()
    return False


def author_follow(from_user, to_user):
    if not author_is_follow(from_user, to_user):
        from_user.following_set.create(to_user=to_user)


def author_unfollow(from_user, to_user):
    from_user.following_set.filter(to_user=to_user).delete()


def on_app_ready(sender, **kwargs):
    def is_follow(self, to_user):
        return author_is_follow(self, to_user)
    setattr(get_user_model(), 'is_follow', is_follow)

    def follow(self, to_user):
        author_follow(self, to_user)
    setattr(get_user_model(), 'follow', follow)

    def unfollow(self, to_user):
        author_unfollow(self, to_user)
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
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField()

    # django gis모듈에서는 "경도,위도" 순서로 저장하므로,
    # 차후 호환성을 위해 "경도/위도" 순으로 저장토록 한다.
    lnglat = models.CharField(max_length=50, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

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
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-id',)

    def as_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

