from django.db.migrations import serializer
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict

from reports.models import Category
from reports.serializers import CategorySerializer, TagSerializer
from .models import Service

from rest_framework.exceptions import ValidationError



class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)

    class Meta:
        model = Service
        fields = 'id name cost'.split()
        # fields = '__all__'


class ServiceDetailSerializer(serializer.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = 'id name cost'.split()
        depth = 1

    def get_tags(self, service):
        return (tag.name for tag in service.tags.all())


class ServiceValidSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3, max_length=255)
    field = serializers.CharField(required=False, default='No text')
    cost = serializers.FloatField(min_value=1, max_value=1000000000)
    is_active = serializers.BooleanField()
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


class ModelSerializer:
    pass


class SerializerMethodField:
    pass