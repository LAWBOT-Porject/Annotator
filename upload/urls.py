from django.urls import path
from .views import upload_view

app_name = 'upload'
urlpatterns = [
    path('', upload_view, name='upload'),
]
