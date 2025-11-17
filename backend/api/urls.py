from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('query/', views.process_query, name='process_query'),
    path('areas/', views.get_available_areas, name='get_available_areas'),
    path('export/', views.export_data, name='export_data'),
]
