from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm, CsvUploadForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
import re
import io
from django.db import models
from users.models import UserRole
from django.contrib import messages


# Create your views here.
@login_required
def customers_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__customers'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard')
    
    customer_list = Customer.objects.all()

    id_customer = request.GET.get('id_customer')
    legal_name = request.GET.get('legal_name')
    country = request.GET.get('country')
    status = request.GET.get('status')

    if id_customer:
        customer_list = customer_list.filter(id_customer__icontains=id_customer)
    if legal_name:
        customer_list = customer_list.filter(legal_name__icontains=legal_name)
    if country:
        customer_list = customer_list.filter(country__icontains=country)
    if status:
        customer_list = customer_list.filter(status__icontains=status)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(['Customer ID', 'Legal Name', 'Name', 'Tax ID', 'Country', 'State/Province', 'City', 'Created By', 'Created At', 'Updated At'])

        for customer in customer_list:
            writer.writerow([
                customer.id_customer, 
                customer.legal_name, 
                customer.name, 
                customer.tax_id,
                customer.country,
                customer.state_province,
                customer.city,
                customer.address,
                customer.zip_code,
                customer.phone,
                customer.email,
                customer.contact_name,
                customer.contact_role,
                customer.category,
                customer.payment_terms,
                customer.currency,
                customer.payment_method,
                customer.bank_account,
                customer.created_by.username if customer.created_by else 'N/A',
                customer.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                customer.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        return response

    paginator = Paginator(customer_list, 10)  # Show 10 customers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers/customer_list.html', {'page_obj': page_obj})

@login_required
def customer_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__suppliers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('customers') # Redirect to suppliers if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            return redirect('customers:customer_create')
    else:
        form = CustomerForm()
        
    return render(request, 'customers/customer_form.html', {'form': form})

@login_required
def customer_edit(request, pk):

    customer = get_object_or_404(Customer, pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__customers'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('customers') # Redirect to customers if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    customer = Customer.objects.get(pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
    }

    return render(request, 'customers/customer_form.html', context)

@login_required
def customer_delete(request, pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__customers'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('customers:customer_list') # Redirect to customers if no permission

    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('customers:customer_list')

    return redirect('customers:customer_list')


@login_required
def customer_bulk_create(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__customers'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('customers:customer_list')

    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                data_set = csv_file.read().decode('UTF-8')
            except UnicodeDecodeError:
                try:
                    csv_file.seek(0)  # Reset file pointer to the beginning
                    data_set = csv_file.read().decode('ISO-8859-1')
                except Exception as e:
                    return render(request, 'customers/customer_bulk_upload.html', {'form': form})

            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)

            if reader.fieldnames:
                if reader.fieldnames[0].startswith('\ufeff'):
                    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

                cleaned_fieldnames = [key.strip() for key in reader.fieldnames]
                reader.fieldnames = cleaned_fieldnames

            successful_records = []
            error_records = []
            customers_to_create = []

            for i, row in enumerate(reader):
                row_number = i + 2
                form_data = {}

                for key, value in row.items():
                    cleaned_value = value.strip() if isinstance(value, str) else value
                    form_data[key] = cleaned_value
                    
                form = CustomerForm(form_data)

                if form.is_valid():
                    customer = form.save(commit=False)
                    customer.created_by = request.user
                    customers_to_create.append(customer)
                    successful_records.append({'row': row_number, 'data': form_data})
                else:
                    errors = {
                        field:', '.join(err)
                        for field, err in form.errors.items()
                    }
                    error_records.append({
                        'row': row_number,
                        'data': form_data,
                        'errors': errors
                    })

            if customers_to_create:
                Customer.objects.bulk_create(customers_to_create)

            messages.success(request, f"Processed {len(successful_records)} customers created successfully.")

            context = {
                'form': form,
                'successful_count': len(successful_records),
                'error_count': len(error_records),
                'total_rows': len(successful_records) + len(error_records),
                'error_records': error_records,
                'successful_records': successful_records,
                'report_generated': True,
            }

            return render(request, 'customers/customer_bulk_upload.html', context)

        return render(request, 'customers/customer_bulk_upload.html', {'form': form})

    else:
        form = CsvUploadForm()
        return render(request, 'customers/customer_bulk_upload.html', {'form': form})

@login_required
def download_template_customers(request):

    header_fields = ['id_customer', 'legal_name', 'name', 'tax_id', 'country', 'state_province', 'city', 'address', 'zip_code', 'phone', 'email', 'contact_name', 'contact_role', 
                     'category', 'payment_terms', 'currency', 'payment_method', 'bank_account','status']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers_template.csv"'

    writer = csv.writer(response)
    writer.writerow(header_fields)

    return response

    

