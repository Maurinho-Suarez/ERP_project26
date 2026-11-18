from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('create/', views.inventory_create, name='inventory_create'),
    path('<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    path('bulk-upload/', views.inventory_bulk_upload, name='inventory_bulk_upload'),
    path('bulk/template/', views.download_template_inventory, name='download_template_inventory'),
]