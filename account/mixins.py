from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from blog.models import Article
from account.models import User

class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            'author', 'slug', 'title', 'category', 'excerpt', 'description', 'photo', 'publish', 'is_special', 'status'
        ]
        if request.user.is_superuser:
            self.fields += ['author']
        return super().dispatch(request, *args, **kwargs)

class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save(self)
        else:
            self.objects = form.save(commit=False)
            self.objects.author = self.request.user
            if not self.objects.status == 'i':
                self.objects.status = ['d']
        return super().form_valid(form)

class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        article = get_object_or_404(Article, pk=pk)
        if (article.author == request.user and article.status in ['b', 'd'] or
        request.user.is_superuser):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید")

class AuthorsAccessMixin():
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect("account:login")
class SuperUserAccessMixin():
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("شما به این صفحه دسترسی ندارید")



