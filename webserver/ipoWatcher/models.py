from django.db import models
import datetime


class Watcher(models.Model):
    email = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    threshold = models.IntegerField(default=5)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class Project(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=150)
    checked = models.BooleanField(default=False)
    downloaded = models.DateField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

