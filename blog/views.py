from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from account.models import User
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from account.mixins import AuthorAccessMixin
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.decorators import method_decorator
from .form import ContactForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

#
class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class ArticleList(ListView):
    # model = Article
    template_name = "blog/home.html"
    # context_object_name = 'articles'
    queryset = Article.objects.published()
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        users = Article.objects.published()
        paginator = self.paginator_class(users, self.paginate_by)

        users = paginator.page(page)

        context['users'] = users
        return context


class ArticleDetail(DetailView):
    template_name = "blog/article_detail.html"
    def get_object(self):
        slug = self.kwargs.get("slug")
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address

        if ip_address not in article.hits.all():
            article.hits.add(ip_address)


        return article

class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 3
    template_name = "blog/category_list.html"
    def get_queryset(self):
        global category
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class AuthorList(ListView):
    paginate_by = 3
    template_name = "blog/author_list.html"
    def get_queryset(self):
        global author
        username = self.kwargs.get("username")
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


@csrf_exempt
def search_feature(request):
    # Check if the request is a post request.
    if request.method == 'POST':
        # Retrieve the search query entered by the user
        search_query = request.POST['search_query']
        # Filter your model by the search query
        posts = Article.objects.filter(
            Q(title__icontains=search_query)
            | Q(excerpt__icontains=search_query)
            | Q(author__username__icontains=search_query)
            | Q(category__title__icontains=search_query)
            | Q(description__icontains=search_query)
        )
        return render(request, 'blog/search.html', {'query':search_query, 'posts':posts})
    else:
        return render(request, 'blog/search.html',{})


class ContactFormView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')
    success_message = 'پیام شما با موفیت ارسال شد.'

    def form_valid(self, form):
        current_site = get_current_site(self.request)

        mail_subject = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        to_email = "sina.raeisi1382@gmail.com"
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'blog/contact_send.html')

# Create your views here.
