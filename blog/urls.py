from django.urls import path
from .views import (
    ArticleList,
    CategoryList,
    ArticleDetail,
    AuthorList,
    ArticlePreview,
    ContactFormView,
)
from . import views

app_name = 'blog'
urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('page/<int:page>', ArticleList.as_view(), name='home'),
    path('article/<str:slug>', ArticleDetail.as_view(), name='article-detail'),
    path('preview/<int:pk>', ArticlePreview.as_view(), name='preview'),
    path('category/<str:slug>', CategoryList.as_view(), name='category'),
    path('category/<str:slug>/page/<int:page>', CategoryList.as_view(), name='category'),
    path('author/<str:username>', AuthorList.as_view(), name='author'),
    path('author/<str:username>/page/<int:page>', AuthorList.as_view(), name='author'),

    path('search/', views.search_feature, name='search-view'),

]