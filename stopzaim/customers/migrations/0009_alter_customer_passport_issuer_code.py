# Generated by Django 4.2.7 on 2023-11-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0008_customer_application_date_alter_customer_address_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="passport_issuer_code",
            field=models.CharField(
                default="", max_length=6, verbose_name="код подразделения"
            ),
        ),
    ]
