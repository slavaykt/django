# Generated by Django 4.2.7 on 2023-12-01 08:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0010_remove_customerrealty_cost_customer_is_married_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="sex",
            new_name="gender",
        ),
        migrations.RenameField(
            model_name="customerchild",
            old_name="sex",
            new_name="gender",
        ),
    ]
