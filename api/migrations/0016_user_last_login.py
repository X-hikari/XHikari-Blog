# Generated by Django 5.1.3 on 2025-03-18 06:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0015_rename_user_id_message_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
