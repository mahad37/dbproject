# Generated by Django 3.0.8 on 2020-12-20 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_auto_20201221_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='product',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
