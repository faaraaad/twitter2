# Generated by Django 4.2.4 on 2023-09-10 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="followership",
            name="created_at",
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]