"""realestate_chatbot URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Real Estate Analysis Chatbot API',
        'version': '1.0',
        'endpoints': {
            'upload': '/api/upload/',
            'query': '/api/query/',
            'areas': '/api/areas/',
            'export': '/api/export/',
        }
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
