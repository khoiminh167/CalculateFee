# Generated by Django 4.2 on 2024-11-14 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='drink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drink_name', models.CharField(max_length=50)),
                ('drink_image', models.ImageField(blank=True, upload_to='photos/drink/drinks/')),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_name', models.CharField(max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('user_image', models.ImageField(blank=True, upload_to='photos/drink/drink_user/')),
            ],
        ),
        migrations.CreateModel(
            name='orderdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('total', models.IntegerField()),
                ('drink_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculateFee.drink')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculateFee.order')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculateFee.user')),
            ],
        ),
    ]
