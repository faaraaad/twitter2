# Generated by Django 4.2.4 on 2023-09-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0002_followership_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="followership",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]