from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey, ManyToManyField


class User(AbstractUser):
   pass

class Listing(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description   = models.CharField(max_length=3000)
    photo = models.CharField(max_length=3000)
    category = models.CharField(max_length=128)
    watchlist = models.ManyToManyField(User, related_name="watchlist")
    starting_bid = models.IntegerField()
    listing_date = models.DateField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User,null=True,on_delete=models.CASCADE, related_name="winner")



class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    Listing =  models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.CharField(max_length=256)


class Bid(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    Listing =  models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid = models.IntegerField()
    



