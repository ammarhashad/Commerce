from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=100)
    starting_bid = models.FloatField()
    image_url = models.TextField()
    category  = models.CharField(max_length=64)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    close = models.BooleanField(default=False)
    Watchlist = models.ManyToManyField(User,blank=True,related_name="Watchlist")

class Bid(models.Model):
    bid = models.FloatField()
    Which_bid = models.ManyToManyField(Listings,blank=True,related_name="bids")
    how_bid = models.ManyToManyField(User,blank=True,related_name="bids")
    bid_date = models.DateTimeField(auto_now_add=True, blank=True)



class Comment(models.Model):
    comment = models.TextField()
    how_comment = models.ManyToManyField(User,blank=True,related_name="comment")
    list_comment = models.ManyToManyField(Listings,blank=True,related_name="comment")
    comment_date = models.DateTimeField(auto_now_add=True, blank=True)
