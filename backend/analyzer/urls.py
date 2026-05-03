from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.get_templates),
    path('templates/<str:doc_type>/', views.get_template_detail),
    path('analyze/', views.analyze_document),
]