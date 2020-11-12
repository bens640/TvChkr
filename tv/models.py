from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Show(models.Model):
    title = models.CharField(max_length=100, default="Title")
    airdate = models.DateTimeField(default=timezone.now)
    genre = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tv-detail', kwargs={'pk': self.pk})



