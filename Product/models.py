from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse

from Register.models import Profile


def create_slug(title):  # new
    slug = slugify(title)
    qs = Product.objects.filter(slug=slug)
    if qs:
        exists = qs.exists()
        if exists:
            slug = "%s-%s" % (slug, qs.first().id)
    return slug


class CategoryGroup(models.Model):
    name = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=2000)
    def get_absolute_url(self):
        return reverse('product:group_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    groupCategory = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=2000)
    slug = models.SlugField(max_length=2000)
    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('product:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=9)
    caption = models.TextField(max_length=2000)
    like = models.IntegerField(default=0)
    percent = models.DecimalField(max_digits=19, decimal_places=9, default=0)
    slug = models.SlugField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='product/products', blank=True, null=True, max_length=2000)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = create_slug(self.title)
        return super().save(*args, **kwargs)

    def get_display_price(self):
        return "{0:.2f}".format(self.price/200)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/products', blank=True, null=True)

class Video(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.CharField(max_length=2000, null=True)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="comment_person")
    comment = models.TextField()

    def __str__(self) -> str:
        return self.user.get_full_name()


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product.title