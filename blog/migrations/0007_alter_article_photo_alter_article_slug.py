# Generated by Django 5.0.7 on 2024-08-01 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='photo',
            field=models.ImageField(upload_to='media', verbose_name='آدرس عکس پست'),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=100, unique=True, verbose_name='آدرس پست'),
        ),
    ]
