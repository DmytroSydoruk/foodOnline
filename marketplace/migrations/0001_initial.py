# Generated by Django 4.1.5 on 2023-01-22 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("menu", "0003_alter_fooditem_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                (
                    "fooitem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.fooditem"
                    ),
                ),
            ],
        ),
    ]
