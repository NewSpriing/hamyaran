# Generated by Django 5.1.4 on 2024-12-31 13:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0034_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)], verbose_name='روز تولد'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthmonth',
            field=models.CharField(blank=True, choices=[('فروردین', 'فروردین'), ('اردیبهشت', 'اردیبهشت'), ('خرداد', 'خرداد'), ('تیر', 'تیر'), ('مرداد', 'مرداد'), ('شهریور', 'شهریور'), ('مهر', 'مهر'), ('آبان', 'آبان'), ('آذر', 'آذر'), ('دی', 'دی'), ('بهمن', 'بهمن'), ('اسفند', 'اسفند')], max_length=15, null=True, verbose_name='ماه تولد'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthyear',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1300), django.core.validators.MaxValueValidator(1450)], verbose_name='سال تولد'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('زن', 'زن'), ('مرد', 'مرد')], max_length=3, null=True, verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='شماره همراه'),
        ),
    ]
