import service
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, viewsets, generics
from services.models import Service
from .serializers import (ServiceSerializer,
                          ServiceDetailSerializer,
                          ServiceValidSerializer)
from rest_framework import status


@api_view(['GET', 'POST'])
def service_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect products from DB
        services = Service.objects.all()
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
                        data=ServiceSerializer(service).data)


@api_view(['GET', 'PUT', 'DELETE'])
def service_detail_api_view(request, id):
    try:
        services: Service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Service not found'})

    if request.method == 'GET':
        data = ServiceSerializer(service).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = ServiceValidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service.text = serializer.validated_data.get('text')
        service.field = serializer.validated_data.get('field')
        service.cost = serializer.validated_data.get('cost')
        service.is_active = serializer.validated_data.get('is_active')
        service.category_id = serializer.validated_data.get('category_id')
        service.tags.set(serializer.validated_data.get('tags'))
        service.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ServiceSerializer(service).data)

    elif request.method == 'DELETE':
        service.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
