# Generated by Django 3.2.16 on 2023-07-24 20:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0007_alter_post_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="comment",
            field=models.ManyToManyField(
                related_name="posts",
                to="blog.Comment",
                verbose_name="Комментарии",
            ),
        ),
    ]
