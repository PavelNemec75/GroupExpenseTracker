from django.db import models  # noqa F401


# Create your models here.

class Posts(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
