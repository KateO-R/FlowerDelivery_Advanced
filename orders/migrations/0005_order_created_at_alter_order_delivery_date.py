# Generated by Django 5.1.4 on 2025-01-30 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_delivery_address_order_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2025-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
