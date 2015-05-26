from django import forms
from blog.models import Post, Comment
from blog.widgets import PointWidget
from blog.utils import square_image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'jjal', 'lnglat')
        widgets = {
            'lnglat': PointWidget,
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def clean_jjal(self):
        jjal = self.cleaned_data['jjal']  # ImageFieldFile instance
        if jjal:
            # jjal.file = thumbnail(jjal.file, 400, 400)
            jjal.file = square_image(jjal.file, 400)
        return jjal

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        if self.author is not None:
            post.author = self.author
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2}),
        }

