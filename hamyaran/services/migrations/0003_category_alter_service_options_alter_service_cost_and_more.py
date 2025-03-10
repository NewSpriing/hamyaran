# Generated by Django 4.2.16 on 2024-12-02 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_therapist'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='دسته بندی')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس')),
                ('status', models.BooleanField(default=True, verbose_name='نمایش داده شود؟')),
                ('position', models.IntegerField(verbose_name='پوزیشن')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ['position'],
            },
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'خدمت', 'verbose_name_plural': 'خدمات'},
        ),
        migrations.AlterField(
            model_name='service',
            name='cost',
            field=models.IntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.TextField(verbose_name='نام خدمت'),
        ),
        migrations.AlterField(
            model_name='service',
            name='therapist',
            field=models.IntegerField(verbose_name='سهم درمانگر'),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=100, verbose_name='دسته بندی'),
        ),
    ]
