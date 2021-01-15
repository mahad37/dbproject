from django.contrib.auth.models import AbstractUser
from django.db import models
from django_pgviews import view as pg

class User(AbstractUser):
    pass

class Listings(models.Model):
    category_choices=(
    ('A','Arts and Crafts'),
    ('E','Electronic Appliances'),
    ('M','Mens Fashion'),
    ('W','Womens Fashion'),
    ('G','Gadgets'),
    ('S','Sports'),
    ('O','Others')
    )
    created_by=models.ForeignKey(User,null=True,related_name='created_by',on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    date=models.DateField()
    starting_bid=models.IntegerField()
    Categories=models.CharField(choices=category_choices, max_length=10)
    image= models.ImageField(upload_to='images/', null=True)
    watchlist=models.BooleanField(null=True)
    highest_bidder=models.ForeignKey(User,null=True,related_name='highest_bidder', on_delete=models.CASCADE)
    close_bid= models.BooleanField(null=True)


    def __str__(self):
        return f"{self.id}: {self.title}, {self.description}, {self.date}, {self.starting_bid}, {self.Categories}"

class Comments(models.Model):
    user=models.ForeignKey(User,null=True,related_name='user',on_delete=models.CASCADE)
    comment=models.CharField(null=True, max_length=500)
    item_id=models.ForeignKey(Listings,null=True,related_name='item_id',on_delete=models.CASCADE)
    date=date=models.DateField(null=True)


class Test(models.Model):
    product= models.CharField(null=True, max_length=100)
    date=models.CharField(null=True,max_length=200)
    amount=models.IntegerField(null=True)
    class Meta:
      managed = False
      db_table = 'test'



class Bids(models.Model):
    user=models.ForeignKey(User,null=True,related_name='bid_user',on_delete=models.CASCADE)
    bid=models.IntegerField(null=True)
    item_id=models.ForeignKey(Listings,null=True,related_name='bid_item_id',on_delete=models.CASCADE)

class Transactions(models.Model):
    product = models.CharField(null=True,max_length=200)
    seller= models.ForeignKey(User,related_name='seller', on_delete=models.CASCADE)
    buyer= models.ForeignKey(User,related_name='buyer', on_delete=models.CASCADE)
    date = models.CharField(null=True,max_length=200)
    city = models.CharField(null=True,max_length=100)
    postal = models.IntegerField(null=True)
    amount=models.IntegerField(null=True)
