from django.db import models


# Create your models here


class Service(models.Model):
    MultiValueError = None
    name = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name






