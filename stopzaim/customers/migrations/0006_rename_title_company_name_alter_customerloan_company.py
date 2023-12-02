# Generated by Django 4.2.7 on 2023-11-27 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("customers", "0005_rename_name_company_title"),
    ]

    operations = [
        migrations.RenameField(
            model_name="company",
            old_name="title",
            new_name="name",
        ),
        migrations.AlterField(
            model_name="customerloan",
            name="company",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="customers.company",
            ),
        ),
    ]
