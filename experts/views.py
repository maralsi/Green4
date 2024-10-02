from django.contrib.auth import authenticate
from django.template.context_processors import request
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.serializers import UserAuthSerializer, UserCreateSerializer
from .models import Expert
from rest_framework import serializers
from rest_framework import status
import experts
from experts.models import Expert
from .serializers import (ExpertSerializer,
                          ExpertDetailSerializer,
                          ExpertValidSerializer)

from rest_framework.views import APIView
# Create your views here.

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


class ExpertSerializer:
    pass


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
                        data=ExpertSerializer(expert).data)

    elif request.method == 'DELETE':
        expert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpertAuthSerializer:
    def __init__(self):
        self.validated_data = None

    pass

    def is_valid(self, raise_exception):
        pass


class AuthApiView(APIView):
    def post(self, request):
# Validation
    serializer = ExpertAuthSerializer()
    serializer.is_valid(raise_exception=True)

    # Authentication
    expert = authenticate(**serializer.validated_data)


class ExpertCreateSerializer:
    pass


@api_view(['POST'])
def registration_api_view(request):
    # Validation
    serializer = ExpertCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Create user
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    email = serializer.validated_data['email']
    expert = Expert.objects.create_expert(username=username, email=email, password=password)

    # Return Response

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': expert.id})
