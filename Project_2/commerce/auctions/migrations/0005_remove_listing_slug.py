# Generated by Django 5.0 on 2024-01-09 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_slug_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='slug',
        ),
    ]