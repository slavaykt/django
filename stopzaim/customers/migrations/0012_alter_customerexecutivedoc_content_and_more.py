# Generated by Django 4.2.7 on 2023-12-02 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0011_rename_sex_customer_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerexecutivedoc",
            name="content",
            field=models.CharField(
                default="", max_length=255, verbose_name="Содержание"
            ),
        ),
        migrations.AlterField(
            model_name="customerexecutivedoc",
            name="executor",
            field=models.CharField(
                default="", max_length=100, verbose_name="Исполнитель"
            ),
        ),
    ]