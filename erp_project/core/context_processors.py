from users.models import UserRole

def get_permissions(request):
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

    roles = []

    if request.user.is_authenticated:
        user_roles = UserRole.objects.filter(user_id=request.user.pk)

        roles = [ur.role.role_name for ur in user_roles]
        for user_role in user_roles:
            role = user_role.role
            for module in permissions.keys():
                current_permission = getattr(role, module, 0)
                if current_permission > permissions[module]:
                    permissions[module] = current_permission


    return {'permissions': permissions, 'roles': roles}
