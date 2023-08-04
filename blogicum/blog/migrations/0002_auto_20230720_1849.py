# Generated by Django 3.2.16 on 2023-07-20 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="posts_images", verbose_name="Фото"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Добавлено"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="category",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Снимите галочку, чтобы скрыть публикацию.",
                verbose_name="Опубликовано",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(
                help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.",
                unique=True,
                verbose_name="Идентификатор",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="title",
            field=models.CharField(max_length=256, verbose_name="Заголовок"),
        ),
        migrations.AlterField(
            model_name="location",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Добавлено"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Снимите галочку, чтобы скрыть публикацию.",
                verbose_name="Опубликовано",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(
                max_length=256, verbose_name="Название места"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Автор публикации",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="blog.category",
                verbose_name="Категория",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Добавлено"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="is_published",
            field=models.BooleanField(
                default=True,
                help_text="Снимите галочку, чтобы скрыть публикацию.",
                verbose_name="Опубликовано",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(
                help_text="Если установить дату и время в будущем — можно делать отложенные публикации.",
                verbose_name="Дата и время публикации",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(verbose_name="Текст"),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=256, verbose_name="Заголовок"),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(verbose_name="Оставить комментарий"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog.post",
                    ),
                ),
            ],
            options={
                "ordering": ("created_at",),
            },
        ),
    ]
