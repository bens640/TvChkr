from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from users.models import Group


class Show(models.Model):
    title = models.CharField(max_length=100, default="Title")
    airdate = models.DateTimeField(default=timezone.now)
    genre = models.CharField(max_length=100)
    poster_path = models.CharField(max_length=100, default="Title")
    show_num = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tv-detail', kwargs={'pk': self.pk})


class StShow(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
