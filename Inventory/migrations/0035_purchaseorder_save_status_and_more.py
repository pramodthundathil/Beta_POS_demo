# Generated by Django 5.0.6 on 2024-11-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0034_rename_tax_purchaseorder_total_discount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='save_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='total_amount_before_discount',
            field=models.FloatField(default=0),
        ),
    ]
