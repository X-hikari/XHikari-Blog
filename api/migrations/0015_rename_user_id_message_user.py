# Generated by Django 5.1.3 on 2025-03-10 02:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0014_message"),
    ]

    operations = [
        migrations.RenameField(
            model_name="message",
            old_name="user_id",
            new_name="user",
        ),
    ]
