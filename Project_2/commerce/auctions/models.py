from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Catergory(models.Model):
    catergory_name = models.CharField(max_length = 50)
    def __str__(self):
        return f"{self.catergory_name}"

class Bid(models.Model):
    bid = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True,related_name='userBid')
    def __str__(self):
        return f"{self.user} has bid $ {self.bid}"
    
class Listing(models.Model):
    title = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    image_link = models.CharField(max_length = 500)
    #starting_bid = models.FloatField()
    bid_price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid_price")
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "owner")
    category = models.ForeignKey(Catergory,on_delete = models.CASCADE, related_name = "listing_category")
    isActive = models.BooleanField(default=True)
    watch_list = models.ManyToManyField(User, blank=True, related_name="watch_list" )
    def __str__(self):
        return f"Listing {self.title}, created by {self.owner}: {self.description}. {self.bid_price.user}  has bid of {self.bid_price.bid}"
    
class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='writer')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing')
    comment = models.CharField(max_length = 100)
    def __str__(self):
        return f"{self.writer} has commented {self.comment} on {self.listing}"