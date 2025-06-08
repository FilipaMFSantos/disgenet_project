from django.urls import path
from . import views

urlpatterns = [
    path('', views.about_page, name='home'),
    path('genes/', views.gene_list, name='gene_list'),
    path('grafico/', views.evolution_chart, name='evolution_chart'),
    path('disease_info/', views.disease_info, name='disease_info'),
    path('about/', views.about_page, name='about'),
]
