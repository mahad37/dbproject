# Generated by Django 3.0.8 on 2020-08-15 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_listings_highest_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='highest_bidder',
            field=models.CharField(max_length=100, null=True),
        ),
    ]