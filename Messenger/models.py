from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse


class MessageRoom(models.Model):
    slug = models.SlugField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_user", null=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_person", null=True)
    def __str__(self) -> str:
        return self.slug

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            slug = str(''.join(str(ord(c)) for c in str(self.user.username)) + ''.join(str(ord(c)) for c in str(self.person.username)))
            self.slug = slugify(slug)
        return super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('messenger:messenger', kwargs={'slug': self.slug})

class Message(models.Model):
    room = models.ForeignKey(MessageRoom, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.room.slug


