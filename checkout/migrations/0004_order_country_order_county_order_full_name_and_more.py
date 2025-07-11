# Generated by Django 5.2.3 on 2025-07-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(default='Unknown', max_length=40),
        ),
        migrations.AddField(
            model_name='order',
            name='county',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='order',
            name='full_name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='postcode',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address1',
            field=models.CharField(default='Unknown', max_length=80),
        ),
        migrations.AddField(
            model_name='order',
            name='street_address2',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name='order',
            name='town_or_city',
            field=models.CharField(default='Unknown', max_length=40),
        ),
    ]
