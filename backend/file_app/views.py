from django.core.files import File
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .resumeParser import ResumeParser
from .serializers import FileSerializer
from backend.settings import MEDIA_ROOT
from django.http import HttpResponse


class FileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        name = request.query_params.get('name')
        path_to_file = MEDIA_ROOT + '/' + name
        f = open(path_to_file, 'rb')
        file = File(f)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = 'attachment'
        return response

    @api_view(['GET'])
    def some(self):
        some = ResumeParser()
        return HttpResponse(some.some(1, 5))

    @api_view(['GET'])
    def somes(self):
        some = ResumeParser()
        return HttpResponse(some.some(1, 10))
