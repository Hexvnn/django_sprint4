# Generated by Django 3.2.16 on 2023-08-04 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0013_remove_comment_post"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                default=20,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="blog.post",
            ),
            preserve_default=False,
        ),
    ]
