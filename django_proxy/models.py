from django.db import models
from django.contrib.auth.models import User


class VisitedURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(unique=False)
    counter = models.IntegerField(default=0)
    data_sent = models.IntegerField(default=0)
    data_received = models.IntegerField(default=0)


class CreatedSites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(unique=False)
    name = models.CharField(unique=True, max_length=255)
