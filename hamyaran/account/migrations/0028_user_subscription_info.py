# Generated by Django 4.2.17 on 2024-12-30 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_remove_user_subscription_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
