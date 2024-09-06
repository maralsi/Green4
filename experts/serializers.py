from rest_framework import serializers
from .models import Expert

class ExperteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expert
        # fields = 'id name cost'.split()
        fields = '__all__'
