# Generated by Django 3.2.16 on 2023-07-24 19:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0003_auto_20230722_1711"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="comment",
        ),
    ]
