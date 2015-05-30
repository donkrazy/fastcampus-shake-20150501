# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (View, ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from blog.mixins import FormValidMessageMixin


index = ListView.as_view(
    model=get_user_model(),
    context_object_name='author_list',
    template_name='blog/author_list.html')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['author'] = self.object.author
        return context

detail = PostDetailView.as_view()


class PostCreateView(FormValidMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    form_valid_message = '새 포스팅을 저장했습니다.'

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['author'] = self.request.user
        return kwargs

new = login_required(PostCreateView.as_view())


class PostUpdateView(FormValidMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    form_valid_message = '포스팅을 수정했습니다.'

edit = login_required(PostUpdateView.as_view())


class PostDeleteView(FormValidMessageMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    form_valid_message = '포스팅을 삭제했습니다.'

delete = PostDeleteView.as_view()


class PostLikeView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.like(request.user)
        return redirect(request.META['HTTP_REFERER'])

post_like = login_required(PostLikeView.as_view())


class PostUnlikeView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        post.unlike(request.user)
        return redirect(request.META['HTTP_REFERER'])

post_unlike = login_required(PostUnlikeView.as_view())


class CommentCreateView(FormValidMessageMixin, CreateView):
    form_class = CommentForm
    form_valid_message = '새 댓글을 저장했습니다.'

    def get_success_url(self):
        return reverse(self.object.post.get_absolute_url())

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])

        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        if self.request.is_ajax():
            return self.object

        # 아래 호출에서도 form.save() 가 호출된다.
        # 바뀐 내역은 없으나, 이때 update 가 수행된다.
        return super(CommentCreateView, self).form_valid(form)

comment_new = CommentCreateView.as_view()


class CommentUpdateView(FormValidMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    form_valid_message = '댓글을 수정했습니다.'

    def get_success_url(self):
        return reverse(self.object.post.get_absolute_url())

comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(FormValidMessageMixin, DeleteView):
    model = Comment
    form_valid_message = '댓글을 삭제했습니다.'

    def get_success_url(self):
        return reverse(self.object.post.get_absolute_url())

comment_delete = CommentDeleteView.as_view()


class AuthorHomeView(ListView):
    model = Post

    def get_queryset(self):
        self.author = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        qs = super(AuthorHomeView, self).get_queryset()
        return qs.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super(AuthorHomeView, self).get_context_data(**kwargs)
        context['author'] = self.author
        return context

author_home = AuthorHomeView.as_view()


class AuthorFollowView(View):
    def get(self, request, *args, **kwargs):
        author = get_object_or_404(get_user_model(), username=kwargs['username'])
        request.user.follow(author)
        messages.info(request, '팔로우했습니다.')
        return redirect('blog:author_home', kwargs['username'])

follow = login_required(AuthorFollowView.as_view())


class AuthorUnfollowView(View):
    def get(self, request, *args, **kwargs):
        author = get_object_or_404(get_user_model(), username=kwargs['username'])
        request.user.unfollow(author)
        messages.info(request, '언팔했습니다.')
        return redirect('blog:author_home', kwargs['username'])

unfollow = login_required(AuthorUnfollowView.as_view())
