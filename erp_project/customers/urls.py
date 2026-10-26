from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customers_list, name='customers_list'),
    path('create/', views.customer_create, name='customer_create'),
    path('edit/<int:pk>/', views.customer_edit, name='customer_edit'),
    path('delete/<int:pk>/', views.customer_delete, name='customer_delete'),
    path('bulk-create/', views.customer_bulk_create, name='customer_bulk_create'),
    path('bulk/template/', views.download_template_customers, name='download_template_customers'),
]