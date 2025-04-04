# Generated by Django 5.1.3 on 2025-03-20 06:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0017_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebInformation",
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
                ("date", models.DateField(auto_now_add=True, unique=True)),
                ("total_views", models.IntegerField(default=0)),
                ("today_views", models.IntegerField(default=0)),
                ("unique_visitors", models.IntegerField(default=0)),
            ],
        ),
    ]
