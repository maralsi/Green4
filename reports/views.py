from Tools.scripts.fixdiv import report
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, viewsets, generics
from rest_framework import status
from reports.models import Report, Category
from reports.serializers import ReportDetailSerializer
from services.serializers import ServiceValidSerializer


# Create your views here.

class ReportSerializer:
    def __init__(self):
        self.data = None

    pass


@api_view(['GET'])
def report_feedback(request):
    feedback = Report.objects.all()
    serializer = ReportDetailSerializer(feedback, many=True)


@api_view(['GET', 'POST'])
def report_list_api_view(request):
    if request.method == 'GET':
        # step 1: Collect products from DB
        reports = Report.objects.select_related('category').prefetch_related('tags').all()
        # step 2: Reformat products (Query Set) to List of dictionary
        data = ReportSerializer()
        # step 3: Return response
        return Response(data=data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        print(request.data)

        # step 1: Get data from RequestBody
        category = request.data.get('category')
        tags = request.data.get('tag')
        name = request.data.get('name')
        description = request.data.get('description')
        date = request.data.get('date')

        # step 2: Create object of service
        reports = Report.objects.create(
            category=category,
            tags=tags,
            name=name,
            description=description,
            date=date,
        )
        reports.tags.set(tags)
        reports.save()

        # step 3: Return Response
        return Response(status=status.HTTP_201_CREATED,
                        data=ReportSerializer(reports).data)


@api_view(['GET'])
def report_detail_api_view(request, id):
    try:
        reports = Report.objects.get(id=id)
    except Report.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={'error': 'Report not found'})
    if request.method == 'GET':
        data = ReportSerializer(reports).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ServiceValidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reports.category = serializer.validated_data.get('category')
        reports.tags = serializer.validated_data.get('tag')
        reports.name = serializer.validated_data.get('name')
        reports.description = serializer.validated_data.get('description')
        reports.date = serializer.validated_data.get('date')
        reports.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReportSerializer(reports).data)

    elif request.method == 'DELETE':
        reports.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
