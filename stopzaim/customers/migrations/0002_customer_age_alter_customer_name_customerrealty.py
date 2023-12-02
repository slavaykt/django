# Generated by Django 4.2.7 on 2023-11-23 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="age",
            field=models.IntegerField(default=0, verbose_name="Возраст"),
        ),
        migrations.AlterField(
            model_name="customer",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Имя"),
        ),
        migrations.CreateModel(
            name="CustomerRealty",
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
                ("name", models.CharField(max_length=255, verbose_name="Наименование")),
                ("cost", models.IntegerField(default=0, verbose_name="Стоимость")),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customers.customer",
                    ),
                ),
            ],
        ),
    ]
