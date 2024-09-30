from rest_framework import serializers
from .models import Expert
from django.db.migrations import serializer
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.settings import api_settings
from rest_framework.utils.serializer_helpers import ReturnDict

from reports.models import Category
from reports.serializers import CategorySerializer, TagSerializer

from rest_framework.exceptions import ValidationError


class ExpertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        # fields = 'id name cost'.split()
        fields = '__all__'


class ExpertValidSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=255)
    experience = serializers.IntegerField()
    education = serializers.CharField(min_length=3, max_lenght=100)
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


class ExpertDetailSerializer:
    pass