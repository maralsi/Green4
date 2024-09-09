from django.db import models


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


# Create your models here.

class Category(AbstractModel):
    pass


class Tag(AbstractModel):
    pass


class Report(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def category_name(self):
        if self.category:
            return self.category.name
        return "None"

STARS = (
    (i, i * '*') for i in range(1, 6)
)


class Feedback(models.Model):
    text = models.TextField()
    # stars = models.IntegerField(choices=STARS, default=5)
    report = models.ForeignKey(Report, on_delete=models.CASCADE,
                               related_name='feedback')
    rating = models.IntegerField()
    def __str__(self):
        return f'{self.report.name} - {self.rating}'


class Avg:
    pass