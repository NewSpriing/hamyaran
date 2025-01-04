# Generated by Django 4.2.16 on 2024-12-04 05:37

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_alter_service_options_service_status_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-position',), 'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ['-category', '-cost'], 'verbose_name': 'خدمت', 'verbose_name_plural': 'خدمات'},
        ),
        migrations.AlterModelManagers(
            name='service',
            managers=[
                ('cats', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='services', to='services.category', verbose_name='دسته بندی'),
        ),
    ]
