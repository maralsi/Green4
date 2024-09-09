from django.contrib import admin
from .models import Report, Category, Tag, Feedback

# Register your models here.

admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Feedback)


