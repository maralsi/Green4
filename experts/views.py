from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Expert
from rest_framework import serializers
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def expert_list_api_view(request):
    # step 1: Collect products from DB
    experts = Expert.objects.all()

    # step 2: Reformat products (Query Set) to List of dictionary
    data = ExpertSerializer(experts, many=True).data

    # step 3: Return response
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def expert_detail_api_view(request, id):
    try:
        experts = Expert.objects.get(id=id)
    except Expert.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Expert not found'})

    data = ExpertSerializer(expert).data
    return Response(data=data)

