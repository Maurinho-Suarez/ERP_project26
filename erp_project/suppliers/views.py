from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Supplier
from .forms import SupplierForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from django.db import models
from users.models import UserRole


# Create your views here.
@login_required
def suppliers_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard')
    
    supplier_list = Supplier.objects.all()

    id_supplier = request.GET.get('id_supplier')
    name = request.GET.get('name')
    country = request.GET.get('country')
    status = request.GET.get('status')

    if id_supplier:
        supplier_list = supplier_list.filter(id_supplier__icontains=id_supplier)
    if name:
        supplier_list = supplier_list.filter(name__icontains=name)
    if country:
        supplier_list = supplier_list.filter(country__icontains=country)
    if status:
        supplier_list = supplier_list.filter(status__icontains=status)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="suppliers.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(['Supplier ID', 'Legal Name', 'Name', 'Tax ID', 'Country', 'State/Province', 'City', 'Created By', 'Created At', 'Updated At'])

        for supplier in supplier_list:
            writer.writerow([
                supplier.id_supplier, 
                supplier.legal_name, 
                supplier.name, 
                supplier.tax_id,
                supplier.country,
                supplier.state_province,
                supplier.city,
                supplier.address,
                supplier.zip_code,
                supplier.phone,
                supplier.email,
                supplier.contact_name,
                supplier.contact_role,
                supplier.category,
                supplier.payment_terms,
                supplier.currency,
                supplier.payment_method,
                supplier.bank_account,
                supplier.created_by.username if supplier.created_by else 'N/A',
                supplier.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                supplier.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        return response

    paginator = Paginator(supplier_list, 10)  # Show 10 suppliers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'suppliers/supplier_list.html', {'page_obj': page_obj})

@login_required
def supplier_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers') # Redirect to suppliers if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.created_by = request.user
            supplier.save()

            return redirect('suppliers:supplier_create')
    else:
        form = SupplierForm()
        
    return render(request, 'suppliers/supplier_form.html', {'form': form})

@login_required
def supplier_edit(request, pk):

    supplier = get_object_or_404(Supplier, pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('suppliers') # Redirect to suppliers if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    supplier = Supplier.objects.get(pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers:supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    context = {
        'form': form,
        'supplier': supplier,
    }

    return render(request, 'suppliers/supplier_form.html', context)

@login_required
def supplier_delete(request, pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('suppliers:supplier_list') # Redirect to suppliers if no permission
    
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers:supplier_list')
    
    return redirect('suppliers:supplier_list')