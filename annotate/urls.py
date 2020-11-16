from django.urls import path
from .views import annotate_view

app_name = 'annotate'
urlpatterns = [
    path('', annotate_view, name='annotate'),
]
