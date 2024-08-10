from django.contrib import admin
from .models import Article, Category, IPAddress
from django.contrib import messages
from django.utils.translation import ngettext




def make_published(modeladmin, request, queryset):
    updated = queryset.update(status="p")
    modeladmin.message_user(
        request,
        ngettext(
            "%d پست منتشر شد.",
            "%d پست منتشر شدند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )
make_published.short_description = 'انتشار پست های انتخاب شده'

def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status="d")
    modeladmin.message_user(
        request,
        ngettext(
            "%d پست پیش نویس شد.",
            "%d پست پیش نویس شدند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )
make_draft.short_description = 'پیش نویس شدن پست های انتخاب شده'




class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Category, CategoryAdmin)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo_tag', 'slug', 'author', 'is_special', 'status', 'jpublish', 'category_to_str')
    list_filter = (['publish', 'status', 'author'])
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    actions = [make_published, make_draft]

admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)

# Register your models here.
