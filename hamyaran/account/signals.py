from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.utils.timezone import now
from django.core.management.base import BaseCommand
from account.models import Notification, User, Prescription, Reminder
from account.utils import send_push_notification
from services.models import Order
from datetime import timedelta
from celery import shared_task
from push_notifications.models import GCMDevice

@receiver(post_save, sender=Order)
def handle_order_creation(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        address = instance.address
        order_items = instance.service
        phone = instance.user.phone
        preferred_time = str(instance.preferred_time)
        special_condition = instance.special_condition
        created_at = instance.jcreated_time
        order_date = str(instance.order_date)


        def order_for():
            if instance.order_for:
                order_for_name = instance.order_for.name
                order_for_phone =  instance.order_for.phone
                return f'{order_for_name}\n<i class="fas fa-phone-alt"></i>: <a href="tel:{order_for_phone}">{order_for_phone}</a>'
            else:
                return 'خودم'    
 

        # Address details
        address_details = address.detail
        location_link = address.location_link 

        # Superuser Notifications
        superusers = User.objects.filter(is_superuser=True)

        for superuser in superusers:

            message_to_superusers = (
            f"""
            سفارش جدید\n\n
            نام کاربر: {user.get_full_name()}
            برای: {order_for()}
            خدمت درخواستی: {order_items}
            شماره تماس: {f'<a href="tel:{phone}">{phone}</a>'}
            زمان ترجیحی: {preferred_time if preferred_time else 'تعیین نشده'}
            در روز: {order_date if order_date else 'تعیین نشده'}
            شرایط ویژه:\n {special_condition}
            عنوان آدرس: {address.title}
            جزئیات آدرس:\n {address_details}
            لینک نقشه: 
            {f'<a href="{location_link}" target="_blank">باز کردن نقشه</a>' if location_link else 'لینکی در آدرس ثبت نشده است'}
            """
            )
            Notification.objects.create(
                recipient=superuser,
                message=message_to_superusers,
            )
            subscription_info = superuser.subscription_info
            send_push_notification(
                subscription_info=subscription_info,
                title="سفارش جدید ثبت شد",
                body=f"سفارش جدید توسط {user.get_full_name()} برای خدمت {order_items} ثبت شده است."
            )

            # Send Email to superusers
           
            email = EmailMessage(
              subject='سفارش جدید',
              body=render_to_string('emails/order_notification_superuser.html',{
                'user' : user.get_full_name(),
                'service': order_items,
                'preferred_time': preferred_time if preferred_time else 'تعیین نشده',
                'special_condition': special_condition,
                'address_title': address.title,
                'address_details':address_details,
                'created_at': created_at,
                'map': location_link,
              }),
              from_email='acnobahar1@gmail.com',
              to=['acnobahar1@gmail.com'],
            )
            email.content_subtype = 'html'
            email.send()

        # Create notification for user
        message_to_user = (
            f"""سفارش شما با موفقیت ثبت شد
            خدمت درخواستی: {order_items}
            برای:{order_for()}
            در روز: {order_date if order_date else 'تعیین نشده'}
            عنوان آدرس: {address.title} 
            لینک آدرس: {f'<a href="{location_link}" target="_blank">باز کردن نقشه</a>' if location_link else 'لینکی در آدرس ثبت نشده است'}
            """
        )

        Notification.objects.create(
            recipient=user,
            message=message_to_user,
        )
        if user.subscription_info:  # بررسی وجود اطلاعات اشتراک کاربر
            send_push_notification(
                subscription_info=user.subscription_info,
                title="سفارش ثبت شد",
                body=f"سفارش شما برای خدمت {order_items} با موفقیت ثبت شد."
            )


@receiver(post_save, sender=Prescription)
def create_reminders(sender, instance, created, **kwargs):
    if created:
        current_time = instance.start_date
        for i in range(instance.qty):  # ایجاد تعداد `qty` ریمایندر
            Reminder.objects.create(
                prescription=instance,
                user=instance.user,
                reminder_time=current_time,
            )
            current_time += timedelta(hours=instance.interval)


@shared_task
def send_reminder_notifications():
    # یافتن ریمایندرهایی که زمان مصرف آن‌ها رسیده است
    reminders = Reminder.objects.filter(reminder_time__lte=now(), is_taken=False)
    
    for reminder in reminders:
        # یافتن دستگاه‌های مرتبط با کاربر
        devices = GCMDevice.objects.filter(user=reminder.user)
        
        for device in devices:
            device.send_message(
                title="یادآوری دارو",
                message=f"زمان مصرف داروی {reminder.prescription.medicine.name} رسیده است."
            )


def generate_reminders():
    # دریافت تمام نسخه‌ها
    prescriptions = Prescription.objects.all()

    for prescription in prescriptions:
        # محاسبه زمان یادآوری‌های آینده
        current_time = prescription.start_date
        while current_time <= now():
            current_time += timedelta(hours=prescription.interval)

        # بررسی وجود یادآوری
        if not Reminder.objects.filter(prescription=prescription, reminder_time=current_time).exists():
            Reminder.objects.create(
                prescription=prescription,
                user=prescription.user,
                reminder_time=current_time
            )
