# Generated by Django 5.0.7 on 2024-08-02 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_article_author_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='excerpt',
            field=models.TextField(max_length=100, verbose_name=' چکیده مطالب پست'),
        ),
    ]
