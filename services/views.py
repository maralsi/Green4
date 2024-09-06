from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Service
from rest_framework import serializers
from rest_framework import status




# from serializers import ServiceSerializer


from services.models import Service
from .serializers import ServiceSerializer


@api_view(['GET'])
def service_list_api_view(request):
    # step 1: Collect products from DB
    services = Service.objects.all()

    # step 2: Reformat products (Query Set) to List of dictionary
    data = ServiceSerializer(services, many=True).data

    # step 3: Return response
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def service_detail_api_view(request, id):
    try:
        service = Service.objects.get(id=id)
    except Service.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Service not found'})

    data = ServiceSerializer(service).data
    return Response(data=data)