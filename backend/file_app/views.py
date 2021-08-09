import mimetypes
import shutil

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
        # file = File(f)
        mime_type, _ = mimetypes.guess_type(path_to_file)
        response = HttpResponse(f, content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % name
        return response

    @api_view(['GET'])
    def init(self):
      shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
      json = {
        'message': 'Media folder is deleted'
      }
      return HttpResponse(json, status=status.HTTP_200_OK)

