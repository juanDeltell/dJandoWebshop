from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from PIL import Image
from django_countries.fields import CountryField



CATEGORY_CHOISES = (
    ('A', 'All'),
    ('P', 'Phone'),
    ('C', 'Car'),
    ('L', 'Lamp')
)

LABEL_CHOISES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger'),
    ('D', 'default'),
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class Item(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    photo = models.ImageField(upload_to='item_pics', default='default.jpg', null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOISES, max_length=2)
    label = models.CharField(choices=LABEL_CHOISES, max_length=1)
    created_at = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default ='juan')
    slug = models.SlugField()
    
    def __str__(self):
    	return self.name

    
    def save(self):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    def get_absolute_url(self):
        #return reverse('item-detail', kwargs={'pk': self.pk})
        return reverse('product', kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
         return reverse('add_to_cart', kwargs={'pk': self.pk})

    def get_remove_from_cart_url(self):
         return reverse('remove_from_cart', kwargs={'pk': self.pk})



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        if self.item.discount_price == 'null':
            return 0
        else:
            return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Addresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"