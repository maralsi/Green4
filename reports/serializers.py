from django.db.migrations import serializer
from rest_framework import serializers
from services import serializers
from . import models
from rest_framework.exceptions import ErrorDetail
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict

from reports.models import Category
from .models import Report
from .models import Tag, Feedback


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


class ReportValidSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(null=True, blank=True)
    date = serializers.DateTimeField(auto_now_add=True)
    category_id = serializers.IntegerField()
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=1)
    )

    def validate(self, attrs):
        category_id = attrs.get('category_id')
        try:
            Category.objects.get(id=category_id)
        except:
            raise ValidationError('Category does not exist!')
        return attrs

    @property
    def errors(self):
        ret = super().errors
        if isinstance(ret, list) and len(ret) == 1 and getattr(ret[0]):
            detail = ErrorDetail('No data provided', code='null')
            ret = {api_settings.NON_FIELD_ERRORS_KEY: [detail]}
        return ReturnDict(ret, serializer=self)
