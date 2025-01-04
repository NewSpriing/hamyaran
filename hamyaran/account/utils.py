from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from webpush import send_user_notification
from .models import WebPushSubscription, User
from pywebpush import webpush, WebPushException
import json




def send_email(subject, recipient_list, template_name, context):
    message = render_to_string(template_name, context)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )



def send_push_notification(subscription_info, title, body):
    """
    ارسال نوتیفیکیشن وب به کاربران.
    """
    try:
        data = json.dumps({"title": title, "body": body})  # تبدیل دیکشنری به رشته JSON
        webpush(
            subscription_info=subscription_info,
            data=data,  # ارسال رشته JSON
            vapid_private_key="مسیر کلید خصوصی VAPID",
            vapid_claims={"sub": "mailto:your-email@example.com"}
        )
    except WebPushException as ex:
        print(f"Web Push failed: {ex}")
        raise ex
