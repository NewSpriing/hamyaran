# Generated by Django 5.1.4 on 2024-12-31 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, verbose_name='شماره همراه'),
        ),
    ]
