from django.db import models
from django.urls import reverse
from account.models import User
from django.utils import timezone
from extensions.utils import jalali_converter
from django.utils.html import format_html
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


#my manager

class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آیپی')

class Category(models.Model):
    parent = models.ForeignKey('self',default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیر دسته')
    title = models.CharField(max_length=200, verbose_name = 'عنوان دسته بندی')
    slug = models.SlugField(max_length=100,unique=True,allow_unicode=True, verbose_name = 'آدرس دسته بندی')
    status = models.BooleanField(default= True,verbose_name = ' آیا نمایش داده شود؟ ')
    position = models.IntegerField(verbose_name = 'پوزیشن')
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent__id','position']

    def __str__(self):
        return self.title

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        if not self.status:
            for article in self.articles.published():
                article.status = 'd'
                article.save()
        super(Category, self).save(*args, **kwargs)

class Article(models.Model):
    STATUS_CHOICES = (
       ('p', 'منتشر شده'),          # publish
       ('d', 'پیش نویس'),           # draft
       ('i', 'در حال بررسی'),       # investigation
       ('b', 'برگشت داده شده'),     # back
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name="نویسنده")
    title = models.CharField(max_length=200, unique=True,verbose_name = 'عنوان پست')
    slug = models.SlugField(max_length=100,unique=True,allow_unicode=True, verbose_name = 'آدرس پست')
    category = models.ManyToManyField(Category, verbose_name = 'دسته بندی', related_name='articles')
    excerpt = models.TextField(max_length=100, verbose_name = ' چکیده مطالب پست')
    description =CKEditor5Field('متن پست')
    photo = models.ImageField(upload_to='media', verbose_name = 'آدرس عکس پست')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name ='وضعیت انتشار ')
    is_special = models.BooleanField(default=False, verbose_name=' پست ویژه ')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, blank=True, related_name="hits", verbose_name='بازدید ها')

    class Meta:
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:admin-home")

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"


    def photo_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 5px;' src='{}' />".format(self.photo.url))
    photo_tag.short_description = "عکس پست"

    def category_to_str(self):
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = 'دسته بندی'

    objects = ArticleManager()
# Create your models here.

