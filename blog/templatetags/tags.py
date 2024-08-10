from django import template
from blog.models import Category

register = template.Library()
@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category": Category.objects.filter(status=True),
    }

@register.inclusion_tag("partials/link.html")
def link(request, link_name, content, classes):
    return{
        "link_name": link_name,
        "request": request,
        "link": "account:{}".format(link_name),
        "content": content,
        "classes": classes,
    }
