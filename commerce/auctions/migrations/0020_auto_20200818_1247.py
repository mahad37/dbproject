# Generated by Django 3.0.8 on 2020-08-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_delete_closebid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='Categories',
            field=models.CharField(choices=[('T', 'Toys'), ('F', 'Fashion'), ('E', 'Electronics'), ('H', 'Home'), ('S', 'Sports'), ('O', 'Others')], max_length=10),
        ),
    ]
