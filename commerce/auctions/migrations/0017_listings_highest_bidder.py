# Generated by Django 3.0.8 on 2020-08-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20200812_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='highest_bidder',
            field=models.CharField(max_length=200, null=True),
        ),
    ]