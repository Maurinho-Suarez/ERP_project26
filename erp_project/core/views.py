from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import UserRole

@login_required
def dashboard_view(request):

    user_roles = UserRole.objects.filter(user_id=request.user)

    permissions = {
        'customers': 0,
        'suppliers': 0,
        'materials': 0,
        'purchases': 0,
        'sales': 0,
        'inventory': 0,
        'accounting': 0,
        'reporting': 0,

    }

    for user_role in user_roles:
        role = user_role.role
        for module in permissions.keys():
            current_permission = getattr(role, module)
            if current_permission > permissions[module]:
                permissions[module] = current_permission

    context = {
        'user': request.user,
        'permissions': permissions,
        'roles': [user_role.role for user_role in user_roles],
    }
    
    return render(request, 'core/dashboard.html', context)
