"""annotator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from static_pages.views import home_view, about_view
from annotate.views import read_file

urlpatterns = [
    # main pages routing
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('about/', about_view, name='about'),

    # upload routing
    path('upload/', include('upload.urls')),
    # annotate routing
    path('annotate/', include('annotate.urls')),
    path('visualize/', include('visualize.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('organize/', include('organize.urls')),
    
    path('admin/', admin.site.urls),
    # path('<path:file>', read_file,name="file_display"),
]
