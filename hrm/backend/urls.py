"""
URL configuration for hrm_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

def api_welcome(request):
    from django.http import JsonResponse
    return JsonResponse({
        'message': 'HRM Backend API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'employees': '/api/employees/',
            'departments': '/api/departments/',
            'organizational-chart': '/api/organizational-chart/'
        }
    })

urlpatterns = [
    path('', api_welcome, name='api_welcome'),
    path('admin/', admin.site.urls),
    path('api/', include('hrm.urls')),
]
