# Generated by Django 3.2.16 on 2023-08-04 14:08

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0012_alter_post_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="post",
        ),
    ]
