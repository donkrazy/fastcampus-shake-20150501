# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/post_list.html', {
        'post_list': post_list,
    })


def detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comment_form': comment_form,
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, author=request.user)
        if form.is_valid():
            post = form.save()
            messages.info(request, '새 포스팅을 저장했습니다.')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, 'blog/form.html', {
        'form': form,
    })


@login_required
def edit(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.info(request, '포스팅을 수정했습니다.')
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/form.html', {
        'form': form,
    })


def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        post.delete()
        messages.error(request, '포스팅을 삭제했습니다.')
        return redirect('blog:index')
    return render(request, 'blog/post_confirm_delete.html', {
        'post': post,
    })


def comment_new(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            if request.is_ajax():
                return comment
            messages.info(request, '새 댓글을 저장했습니다.')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'blog/form.html', {
        'form': form,
    })


def comment_edit(request, post_id, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            post = form.save()
            messages.info(request, '댓글을 수정했습니다.')
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/form.html', {
        'form': form,
    })


def comment_delete(request, post_id, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        comment.delete()
        messages.error(request, '댓글을 삭제했습니다.')
        return redirect(comment.post.get_absolute_url())
    return render(request, 'blog/comment_confirm_delete.html', {
        'comment': comment,
    })


@login_required
def follow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    request.user.follow(author)
    messages.info(request, '팔로우했습니다.')
    return redirect('blog:author_home', username)


@login_required
def unfollow(request, username):
    author = get_object_or_404(get_user_model(), username=username)
    request.user.unfollow(author)
    messages.info(request, '언팔했습니다.')
    return redirect('blog:author_home', username)
