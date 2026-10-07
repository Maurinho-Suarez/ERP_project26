from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, UserRole

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')

    search_fields = ('username', 'email','first_name', 'last_name')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'customers', 'suppliers', 'materials', 'purchases', 'sales', 'inventory', 'accounting', 'reporting')
    list_filter = ('customers', 'suppliers', 'materials', 'purchases', 'sales', 'inventory', 'accounting', 'reporting') 
    search_fields = ('role_name',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role')
    list_filter = ('role',)
    search_fields = ('user_id__username', 'role__role_name')
