# Generated by Django 3.0.8 on 2020-08-18 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20200815_1940'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CloseBid',
        ),
    ]