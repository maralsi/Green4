from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from reports.models import Report


# Create your views here.

class ReportSerializer:
    pass


@api_view(['GET'])
def report_list_api_view(request):
    # step 1: Collect products from DB
    reports = Report.objects.all()

    # step 2: Reformat products (Query Set) to List of dictionary
    data = ReportSerializer(reports, many=True).data

    # step 3: Return response
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def expert_detail_api_view(request, id):
    try:
        report = Report.objects.get(id=id)
    except Report.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Report not found'})

    data = ReportSerializer(report).data
    return Response(data=data)


def report_list_api_view(request):
    return None