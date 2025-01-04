from django import template
from services.models import Category
from account.models import Notification, Reminder

register = template.Library()

""" @register.simple_tag
def title():
  return
"""

@register.inclusion_tag('registration/partials/category_filter.html')
def sidebar_category_filter():
  return {
    'category': Category.objects.filter(status=True),
  }


@register.inclusion_tag('registration/partials/link.html')
def link(request, link_name, content):
  return {
    'request': request,
    'link_name': link_name,
    'link': 'account:{}'.format(link_name),
    'content': content,
  }

@register.simple_tag
def unread_notification_count(user):
  return Notification.objects.filter(recipient=user, is_read=False).count()  

@register.simple_tag
def unread_reminder_count(user):
  return Reminder.objects.filter(user=user, is_read=False).count()  

@register.filter
def first_n_words(value, n=5):
    """
    Returns the first n words of a string.
    """
    if not isinstance(value, str):
        return value
    words = value.split()
    return " ".join(words[:n])  