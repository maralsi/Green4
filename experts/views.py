from django.template.context_processors import request
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Expert
from rest_framework import serializers
from rest_framework import status
import experts
from experts.models import Expert
from .serializers import (ExpertSerializer,
                          ExpertDetailSerializer,
                          ExpertValidSerializer)


# Create your views here.

class ExpertSerializer:
    pass


@api_view(['GET', 'POST'])
def expert_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect products from DB
        expert = Expert.objects.all()
        # step 2: Reformat products (Query Set) to List of dictionary
        data = ExpertSerializer(expert, many=True).data
        # step 3: Return response
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)

        # step 1: Get data from RequestBody
        name = request.data.get('name')
        experience = request.data.get('experience')
        education = request.data.get('education')
        is_active = request.data.get('is_active')

        # step 2: Create object of service
        expert = Expert.objects.create(
            name=name,
            experience=experience,
            education=education,
            is_active=is_active
        )

        from Tools.scripts.ptags import tags
        expert.tags.set(tags)
        expert.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=ExpertSerializer(expert).data)

@api_view(['GET', 'PUT', 'DELETE'])
def expert_detail_api_view(request, id):
    try:
        expert = Expert.objects.get(id=id)
    except Expert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Expert not found'})
    if request.method == 'GET':
        data = ExpertSerializer(expert).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ExpertValidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        expert.name = serializer.validated_data.get('name')
        expert.experience = serializer.validated_data.get('experience')
        expert.education = serializer.validated_data.get('education')
        expert.is_active = serializer.validated_data.get('is_active')
        expert.save()
        expert.tags.set(serializer.validated_data.get('tags'))
        return Response(status=status.HTTP_201_CREATED,
                        data=ExperteSerializer(expert).data)

    elif request.method == 'DELETE':
        expert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

