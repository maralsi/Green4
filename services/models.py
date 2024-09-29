from django.db import models

from reports.models import Category


# Create your models here


class Service(models.Model):
    MultiValueError = None
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True)  # category_id
    text = models.TextField(null=True, blank=True)
    field = models.CharField(max_length=255, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        if self.category:
            return self.category.name
        return None


STARS = (
    (i, i * '* ') for i in range(1, 6)
)


class Review(models.Model):
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=5)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name='reviews') # service_id

    def __str__(self):
        return self.text
