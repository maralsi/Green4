from Tools.scripts.fixdiv import report
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, viewsets, generics
from rest_framework import status
from reports.models import Report
from reports.serializers import ReportDetailSerializer


# Create your views here.

class ReportSerializer:
    pass


@api_view(['GET'])
def report_feedback(request):
    feedback = Report.objects.all()
    serializer = ReportDetailSerializer(feedback, many=True)



@api_view(['GET'])
def report_list_api_view(request):
    # step 1: Collect products from DB
    reports = Report.objects.select_related('category').prefetch_related('tags').all()

    # step 2: Reformat products (Query Set) to List of dictionary
    data = ReportSerializer()

    # step 3: Return response
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def report_detail_api_view(request, id):
    try:
        reports = Report.objects.get(id=id)
    except Report.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Report not found'})

    data = ReportDetailSerializer(reports, many=False).data
    return Response(data=data)


@api_view(['GET'])
def service_list_api_view(request):
    return None


@api_view(['GET'])
def service_detail_api_view(request):
    return None


@api_view(['GET'])
def expert_list_api_view(request):
    return None


@api_view(['GET'])
def expert_detail_api_view(request):
    return None


def report_feedback_api_view(request):
    return None