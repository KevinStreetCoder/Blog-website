from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
@register.simple_tag
def total_post():
    return Post.published.count()

@register.inclusion_tag('bitcoin/post/latest_post.html')
def show_latest(count =2):
    latest_post = Post.published.order_by('-publish')[:count]

    return {'latest_post': latest_post}

@register.simple_tag
def get_most_commented_post(count = 5):
    return Post.published.annotate(total_comment=Count('comments')).order_by('-total_comment')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

