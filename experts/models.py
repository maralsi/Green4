from django.db import models


# Create your models here.
class Expert(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    education = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
