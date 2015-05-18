# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from blog.mixins import FormValidMessageMixin


index = ListView.as_view(model=Post)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
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


class CommentCreateView(FormValidMessageMixin, CreateView):
    form_class = CommentForm
    form_valid_message = '새 댓글을 저장했습니다.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['id'])

        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        if self.request.is_ajax():
            return self.object

        # 아래 호출에서도 form.save() 가 호출된다.
        # 바뀐 내역은 없으나, 이때 update 가 수행된다.
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_new = CommentCreateView.as_view()


class CommentUpdateView(FormValidMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    form_valid_message = '댓글을 수정했습니다.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(FormValidMessageMixin, DeleteView):
    model = Comment
    form_valid_message = '댓글을 삭제했습니다.'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

comment_delete = CommentDeleteView.as_view()
