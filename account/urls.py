from django.urls import path
from .views import UserRegisterView

#app_name = 'account'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    #path('', upload_view, name='upload'),
]
