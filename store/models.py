from nturl2path import url2pathname
from account import ACCOUNT
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from account.managers import CustomUserManager

# Create your models here.

# class CustomerUser(models.Model):
#     shopuser = models.OneToOneField(ShopUse, null = True, blank = True, on_delete = models.CASCADE)
#     name = models.CharField(max_length = 300, null = True)
#     email = models.EmailField(max_length=300, blank = False, unique = True)
#     def __str__(self):
#         return self.name

# class ShopUser(models.Model):
#     # shopuser = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
#     email = models.EmailField(unique=True)
#     is_staff = models.BooleanField(default=False)
#     is_hidden = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#     name = models.CharField(max_length=200)
#     display_name = models.CharField(max_length=200)
    
#     profile_picture = models.ImageField(upload_to="profiles/", null=True, blank=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'display_name']

#     objects = CustomUserManager()

#     def __str__(self):
#         return self.email

#     def profile_picture_preview(self):
#         if self.profile_picture:
#             return mark_safe(u"<a href='{}'><img height='300' style='border-radius: 50%;' src='{}'/></a>".format(self.profile_picture.url, self.profile_picture.url))
#         else:
#             return 'No Image'
#     profile_picture_preview.short_description = 'Image'

#     def get_name(self):
#         return self.display_name


class Product(models.Model):
    itemname = models.CharField(max_length=250)
    price = models.FloatField()
    image = models.ImageField(null = True, blank = True)
    physical = models.BooleanField(default=True, null=False, blank=False)

    def __str__(self):
        return self.itemname
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):
    customer = models.ForeignKey("account.User", on_delete=models.SET_NULL, blank = True, null = True)
    identification = models.CharField(max_length = 20, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default = False)
    
    def __str__(self):
        return (self.identification)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderedproduct_set.all()
        for i in orderitems:
            if i.product.physical == True:
                shipping = True
            return shipping

    @property
    def get_cart_items(self):
        ordereditems = self.orderedproduct_set.all()
        total = sum([item.quantity for item in ordereditems])
        return total

    @property
    def get_cart_total(self):
        ordereditems = self.orderedproduct_set.all()
        total = sum([item.get_total for item in ordereditems])
        return total

class orderedproduct(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    sold_since = models.DateTimeField(auto_now_add = True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey("account.User", on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length = 300, null = False)
    city = models.CharField(max_length = 100, null = False)
    state = models.CharField(max_length = 75, null = False)
    zipcode = models.CharField(max_length = 20, null = False)

    def __str__(self):
        return (self.address)