# The views used below are normally mapped in the AdminSite instance.
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.


from account import views
from django.urls import path, re_path
from .views import (
    ArticleView,
    LogoutView,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    Profile,
    PasswordChange,
    PasswordChangeDone,
    Register,
)





app_name = 'account'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.SingUpView, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path(
        "password_change/", PasswordChange.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        PasswordChangeDone.as_view(),
        name="password_change_done",
    ),
    path(
        'activate/<slug:uidb64>/<slug:token>/',
        views.activate,
        name='activate'
    )

]

urlpatterns +=[
    path('', ArticleView.as_view(), name='admin-home'),
    path('article/create', ArticleCreate.as_view(), name='create'),
    path('article/update/<int:pk>', ArticleUpdate.as_view(), name='update'),
    path('article/create/<int:pk>', ArticleDelete.as_view(), name='delete'),
    path('profile/', Profile.as_view(), name='profile'),

]
