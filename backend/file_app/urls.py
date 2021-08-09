from django.urls import path
from .views import FileView

urlpatterns = [
    path('upload', FileView.as_view(), name='file-upload'),
    path('download', FileView.as_view(), name='download'),
    path('init', FileView.init, name='init'),
]
