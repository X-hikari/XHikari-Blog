# Generated by Django 5.1.3 on 2025-03-02 08:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_emotion_emotionmedia_emotion_medias_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="emotionmedia",
            options={},
        ),
        migrations.RemoveIndex(
            model_name="emotion",
            name="api_emotion_created_39f085_idx",
        ),
        migrations.RemoveIndex(
            model_name="emotionmedia",
            name="api_emotion_emotion_e31735_idx",
        ),
        migrations.RemoveField(
            model_name="emotion",
            name="medias",
        ),
        migrations.RemoveField(
            model_name="emotionmedia",
            name="media",
        ),
        migrations.RemoveField(
            model_name="emotionmedia",
            name="sort_order",
        ),
        migrations.AddField(
            model_name="emotionmedia",
            name="file",
            field=models.FileField(null=True, upload_to="emotions/"),
        ),
    ]
