from django.db.models import Avg
from rest_framework import serializers

from . import models
from .models import Report, Category, Tag, Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'report', 'rating']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    feedbacks = FeedbackSerializer(many=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Report
        fields = 'id name category tags report feedback'.split()
        # depth = 1
        # fields = '__all__'

    def get_average_rating(self, obj):
        feedbacks = obj.feedbacks.all()
        if feedbacks.exists():
            return feedbacks.aggregate(models.Avg('rating'))['rating__avg']
        return None

class ReportDetailSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = 'id name description date category feedback'.split()
        depth = 1

    def get_tags(self, report):
        return [tag.name for tag in report.tags.all()]

