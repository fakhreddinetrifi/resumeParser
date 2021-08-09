from django.urls import path
from .views import FileView

urlpatterns = [
    path('upload', FileView.as_view(), name='file-upload'),
    path('download', FileView.as_view(), name='download'),
    path('some', FileView.some, name='some'),
    path('somes', FileView.somes, name='somes'),
]
