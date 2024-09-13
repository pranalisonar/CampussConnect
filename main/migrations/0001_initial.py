# Generated by Django 5.1 on 2024-09-01 18:51

import ckeditor.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=120)),
                ('Describe_content', models.CharField(max_length=220, null=True)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('Content', ckeditor.fields.RichTextField()),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='blog_post', to=settings.AUTH_USER_MODEL)),
                ('Category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.posts_category')),
            ],
        ),
    ]
