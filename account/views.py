from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import User
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,

)
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Article
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView
from .mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperUserAccessMixin,
    AuthorsAccessMixin
)
from django.urls import reverse_lazy
from .form import ProfileForm
from django.http import HttpResponse
from account.form import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


@method_decorator(csrf_exempt, name='dispatch')
class ArticleView(AuthorsAccessMixin, ListView):
    template_name = 'registration/home.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/login.html', {'form':AuthenticationForm(), 'error':'نام کاربری با رمز مطابقت ندارد'})
        else:
            login(request, user)
            return redirect('account:admin-home')


# class LogInView(LoginView):
#     queryset = Article.objects.all()
#     template_name = 'registration/login.html'

@csrf_exempt
def SingUpView(request):
    if request.method == 'GET':
        return render(request, 'registration/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('account:login')
            except IntegrityError:
                return render(request, 'registration/signup.html',{'form': UserCreationForm(), 'error': 'نام کاربری مورد نظر قبلا استفاده شده است. لطفا نام کاربری دیگری را انتخاب کنید'})
        else:
            return render(request, 'registration/signup.html', {'form': UserCreationForm(), 'error': 'پسورد مطابقت ندارد'})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(LogoutView):
    template_name = 'blog/home.html'


@method_decorator(csrf_exempt, name='dispatch')
class ArticleCreate(AuthorsAccessMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Article
    template_name = ("registration/article-create-update.html")
@method_decorator(csrf_exempt, name='dispatch')
class ArticleUpdate(AuthorAccessMixin, FormValidMixin , FieldsMixin, UpdateView):
    model = Article
    template_name = "registration/article-create-update.html"

class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("account:admin-home")
    template_name = "registration/article_confirm_delete.html"


class Profile(LoginRequiredMixin,UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs

class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')

class PasswordChangeDone(PasswordChangeDoneView):
    success_url = reverse_lazy('account:profile')


@method_decorator(csrf_exempt, name='dispatch')
class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'registration/active_send.html')
@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/active_done.html')
    else:
        return render(request, 'registration/active_not.html')



# Create your views here.
