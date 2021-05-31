from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Provision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username