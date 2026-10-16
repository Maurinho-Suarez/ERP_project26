from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.suppliers_list, name='suppliers_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    path('bulk-create/', views.supplier_bulk_create, name='supplier_bulk_create'),
    path('bulk/template/', views.dowload_template_suppliers, name='download_template_suppliers'),
]