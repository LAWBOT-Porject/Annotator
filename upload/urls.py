from django.urls import path, re_path
from .views import upload_view
from annotate.views import read_file
app_name = 'upload'
urlpatterns = [
    path('', upload_view, name='upload'),
    #re_path(r'^files_upload.*', read_file, name='read_upload'),
    path('files_uploaded/<str:file>', read_file, name='read_upload'),
]
