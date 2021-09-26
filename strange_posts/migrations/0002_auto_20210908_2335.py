# Generated by Django 3.2.7 on 2021-09-08 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strange_posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория для постов',
                'verbose_name_plural': 'Категории для постов',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(default=[], to='strange_posts.PostCategory'),
        ),
    ]
