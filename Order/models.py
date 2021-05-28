from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify

from Product.models import Product

class State(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=2000, null=True, blank=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_person")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=19, decimal_places=9)
    state = models.ForeignKey(State,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,  null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_complete = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return self.product.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.user)
        return super().save(*args, **kwargs)