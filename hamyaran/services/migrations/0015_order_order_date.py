# Generated by Django 4.2.17 on 2024-12-24 02:04

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_order_order_for'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=django_jalali.db.models.jDateField(blank=True, null=True, verbose_name='انتخاب تاریخ'),
        ),
    ]
