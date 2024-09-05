from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.seller.id, filename)

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length=64)
    date = models.DateTimeField(blank = True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=1000)
    NEW = 'N'
    LIKE_NEW = 'LN'
    USED_GOOD = 'UG'
    USED_FAIR = 'UF'
    USED_POOR = 'UP'
    DAMAGED = 'DMG'
    CONDITION_CHOICES = {
        (NEW, 'New'),
        (LIKE_NEW, 'Like New'),
        (USED_GOOD, 'Used - Good'),
        (USED_FAIR, 'Used - Fair'),
        (USED_POOR, 'Used - Poor'),
        (DAMAGED, 'Damaged',)
    }
    condition = models.CharField(
        max_length=3,
        choices=CONDITION_CHOICES,
    )
    GARDEN_AND_DIY = 'G&DIY'
    CHILD = 'CHLD'
    ELECTRONICS = "ELECT"
    ARTS = 'ARTS'
    ENTERTAINMENT = 'ENTER'
    FASHION = 'FSHN'
    MOTORIZATION = 'AUTO'
    REAL_ESTATES = 'REST'
    BEAUTY = 'BTY'
    CATEGORIES_CHOICES = {
        (GARDEN_AND_DIY, 'Garden & DYI'),
        (CHILD, 'Child'),
        (ELECTRONICS, 'Electronics'),
        (ARTS, 'Arts'),
        (ENTERTAINMENT, 'Entertainment'),
        (FASHION, 'Fashion'),
        (MOTORIZATION, 'Motorization'),
        (REAL_ESTATES, 'Real Estates'),
        (BEAUTY, 'Beauty'),
    }
    category = models.CharField(
        max_length=5,
        choices=CATEGORIES_CHOICES,
    )
    image = models.ImageField(upload_to=user_directory_path)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'listings')
    active = models.BooleanField(default = True)
    sold_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'won_listing', null=True, blank=True)
    sold_for = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid = models.DecimalField(max_digits=12, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return (f"{self.listing} price is {self.bid}. Bidder is {self.bidder}.")

class Comment(models.Model):
    comment = models.CharField(max_length=1000, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    date = models.DateTimeField(blank = True)

    def __str__(self):
        return (f"{self.user} wrote {self.comment} under {self.listing} on {self.date}.")

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_watchlist")
    listing = models.ManyToManyField(Listing, related_name="listings_on_watchlist")

    def __str__(self):
        return (f"{self.user}'s watchlist")
    



