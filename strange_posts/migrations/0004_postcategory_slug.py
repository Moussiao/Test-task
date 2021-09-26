# Generated by Django 3.2.7 on 2021-09-20 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('strange_posts', '0003_auto_20210909_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategory',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now, unique=True, verbose_name='URL'),
            preserve_default=False,
        ),
    ]