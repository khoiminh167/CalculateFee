# Generated by Django 4.2 on 2024-11-19 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculateFee', '0003_remove_orderdetail_drink_id_orderdetail_drink_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='extra_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
