from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('', views.purchases_list, name='purchases_list'),
    path('create/', views.purchase_create, name='purchase_create'),
    path('edit/<int:pk>/', views.purchase_edit, name='purchase_edit'),
    path('delete/<int:pk>/', views.purchase_delete, name='purchase_delete'),
    path('bulk-create/', views.purchase_bulk_create, name='purchase_bulk_create'),
    path('bulk/template/', views.download_template_purchases, name='download_template_purchases'),
]