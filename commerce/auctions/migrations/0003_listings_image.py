# Generated by Django 3.0.8 on 2020-07-27 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='image',
            field=models.ImageField(default='auctions/pictures/none.jpg', upload_to='auctions/pictures/'),
        ),
    ]