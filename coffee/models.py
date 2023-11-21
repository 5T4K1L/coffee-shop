from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


# dummy only for the model Products to work
class Beverage(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=500, default='')
    productImage = models.ImageField(
        upload_to='coffee/media', null=True, blank=True)

    normalprice = models.IntegerField(default=0)
    smallprice = models.IntegerField(default=0)
    mediumprice = models.IntegerField(default=0)
    largeprice = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Beverage, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Products(models.Model):

    best_try = (
        ('MUST TRY', 'MUST TRY'),
        ('BEST PRODUCT', 'BEST PRODUCT'),
    )

    category = (
        ('COLD', 'COLD'),
        ('HOT', 'HOT'),
        ('FOOD', 'FOOD'),
    )

    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.CharField(max_length=500, default='')
    productImage = models.ImageField(
        upload_to='coffee/media', null=True, blank=True, verbose_name="Product Image (Width: 56 | Height: 84)")

    normalprice = models.IntegerField(default=0, verbose_name="Normal Price")
    smallprice = models.IntegerField(default=0, verbose_name="Small Price")
    mediumprice = models.IntegerField(default=0, verbose_name="Medium Price")
    largeprice = models.IntegerField(default=0, verbose_name="Large Price")

    category = models.CharField(blank=False, choices=category, default=False)

    bestProduct = models.CharField(
        blank=True, default='', choices=best_try, verbose_name="Best Product or Must Try | Leave if None")

    class Meta:
        unique_together = ('name', 'slug')
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class OrdersInCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    name = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="product_name")
    size = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(
        upload_to='coffee/media', null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    comment = models.CharField(default='', blank=True, max_length=1000)


class BillingAddress(models.Model):

    isComplete = (
        ('NO', 'NO'),
        ('YES', 'YES'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(default='', null=True, max_length=1000)
    contact_number = models.CharField(default='', null=True, max_length=1000)
    full_address = models.CharField(default='', null=True, max_length=1000)
    message = models.CharField(default='', null=True, max_length=1000)

    total_price = models.CharField(default='', null=True, max_length=1000)

    is_complete = models.CharField(choices=isComplete, null=True, default='')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.full_name:
            self.slug = slugify(self.full_name)
        super(BillingAddress, self).save(*args, **kwargs)


class UsersOrderNotif(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(BillingAddress, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Users' Order Notifications"


class UserProductInAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    prod_name = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="user_products")
    prod_size = models.CharField(max_length=255, null=True, blank=True)
    prod_quantity = models.CharField(max_length=255, null=True, blank=True)
    prod_price = models.CharField(max_length=255, null=True, blank=True)


class Completed(models.Model):
    product_name = models.CharField(default='', null=True, max_length=1000)
    product = models.CharField(default='', null=True, max_length=1000)
    quantity = models.CharField(default='', null=True, max_length=1000)
    full_name = models.CharField(default='', null=True, max_length=1000)
    price = models.CharField(max_length=255, null=True, blank=True)
    date_ordered = models.DateField(default=date.today)
