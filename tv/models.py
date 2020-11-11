from django.db import models
from django.utils import timezone

# Create your models here.

class Show(models.Model):
    title = models.CharField(max_length=100, default="Title")
    airdate = models.DateTimeField(default=timezone.now)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title