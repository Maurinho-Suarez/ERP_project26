from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.suppliers_list, name='suppliers_list'),
    path('create/', views.supplier_create, name='supplier_create'),
    path('detail/<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('update/<int:pk>/', views.supplier_update, name='supplier_update'),
    path('delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
]