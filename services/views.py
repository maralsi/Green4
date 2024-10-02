from collections import OrderedDict

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers, viewsets, generics

from reports.models import Tag
from services.models import Service, Category
from .serializers import (ServiceSerializer,
                          ServiceDetailSerializer,
                          ServiceValidSerializer)
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CategorySerializer, TagSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'


class CategoryListAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPagination


class ServiceListAPIView(ListCreateAPIView):
    serializer_class = ServiceSerializer
    queryset = Service.objects.select_related('category').prefetch_related('tags')

    def post(self, request, *args, **kwargs):
        # step 0: Validation of data
        serializer = ServiceValidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Get data from RequestBody
        text = serializer.validated_data.get('text')
        field = serializer.validated_data.get('field')
        cost = serializer.validated_data.get('cost')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # step 2: Create object of service
        services = Service.objects.create(
            text=text,
            field=field,
            cost=cost,
            is_active=is_active,
            category_id=category_id,
        )
        services.tags.set(tags)
        services.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=ServiceSerializer(services).data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def service_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # step 1: Collect products from DB
        services = Service.objects.select_related('category').prefetch_related('tags')
        # step 2: Reformat products (Query Set) to List of dictionary
        data = ServiceSerializer(instance=services, many=True).data
        # step 3: Return response
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # step 0: Validation of data
        serializer = ServiceValidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # step 1: Get data from RequestBody
        text = request.data.get('text')
        field = request.data.get('field')
        cost = request.data.get('cost')
        is_active = request.data.get('is_active')
        category_id = request.data.get('category_id')
        tags = request.data.get('tags')

        # step 2: Create object of service
        services = Service.objects.create(
            text=text,
            field=field,
            cost=cost,
            is_active=is_active,
            category_id=category_id,
        )
        services.tags.set(tags)
        services.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=ServiceSerializer(services).data)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail_api_view(request, id):
    try:
        services: Service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Service not found'})

    if request.method == 'GET':
        data = ServiceSerializer(services).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ServiceValidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        services.text = serializer.validated_data.get('text')
        services.field = serializer.validated_data.get('field')
        services.cost = serializer.validated_data.get('cost')
        services.is_active = serializer.validated_data.get('is_active')
        services.category_id = serializer.validated_data.get('category_id')
        services.tags.set(serializer.validated_data.get('tags'))
        services.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ServiceSerializer(services).data)

    elif request.method == 'DELETE':
        services.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
