# Generated by Django 5.1.3 on 2025-03-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_alter_emotionmedia_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emotionmedia",
            name="file",
            field=models.FileField(upload_to="emotions/"),
        ),
    ]
