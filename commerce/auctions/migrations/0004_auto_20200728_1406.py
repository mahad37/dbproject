# Generated by Django 3.0.8 on 2020-07-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]