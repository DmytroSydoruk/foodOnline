# Generated by Django 4.1.5 on 2023-01-12 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_user_groups_user_is_superuser_user_user_permissions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_1",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="address_line_2",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="address",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
