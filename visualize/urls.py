from django.urls import path

from .views import visualize_view

urlpatterns = [
    path('', visualize_view, name='visualize'),
]
