# -*- coding: utf8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


index = ListView.as_view(model=Post, template_name='blog/index.html')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

detail = PostDetailView.as_view()


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

    def form_valid(self, form):
        response = super(PostCreateView, self).form_valid(form)
        messages.info(self.request, '새 포스팅을 저장했습니다.')
        return response

new = PostCreateView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

    def form_valid(self, form):
        response = super(PostUpdateView, self).form_valid(form)
        messages.info(self.request, '포스팅을 수정했습니다.')
        return response

edit = PostUpdateView.as_view()


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_delete_confirm.html'
    success_url = reverse_lazy('blog:index')

    def delete(self, request, *args, **kwargs):
        response = super(PostDeleteView, self).delete(request, *args, **kwargs)
        messages.error(self.request, '포스팅을 삭제했습니다.')
        return response

delete = PostDeleteView.as_view()


class CommentCreateView(CreateView):
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['id'])

        self.object = form.save(commit=False)
        self.object.post = post
        self.object.save()

        if self.request.is_ajax():
            return self.object

        messages.info(self.request, '새 댓글을 저장했습니다.')

        # 아래 호출에서도 form.save() 가 호출된다.
        # 바뀐 내역은 없으나, 이때 update 가 수행된다.
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.id])

comment_new = CommentCreateView.as_view()


class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/form.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

    def form_valid(self, form):
        response = super(CommentUpdateView, self).form_valid(form)
        messages.info(self.request, '댓글을 수정했습니다.')
        return response

comment_edit = CommentUpdateView.as_view()


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment_delete_confirm.html'

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.object.post.id])

    def delete(self, request, *args, **kwargs):
        response = super(CommentDeleteView, self).delete(request, *args, **kwargs)
        messages.error(self.request, '댓글을 삭제했습니다.')
        return response

comment_delete = CommentDeleteView.as_view()
