from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    photo = models.ImageField(upload_to='category_pics', blank=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()
        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
           
CATEGORY_CHOISES = (
    ('P', 'Phone'),
    ('C', 'Car'),
    ('L', 'Lamp')
)


LABEL_CHOISES = (
    ('p', 'primary'),
    ('s', 'secondary'),
    ('d', 'danger')
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

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
