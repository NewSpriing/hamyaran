# Generated by Django 4.2.17 on 2024-12-12 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_user_created_time_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='location_link',
            field=models.URLField(blank=True, null=True, verbose_name='لینک گوگل مپ'),
        ),
    ]
