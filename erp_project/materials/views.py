from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Material, Unit, MaterialType, Status
from .forms import MaterialForm, CsvUploadForm
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
def material_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission
    
    material_list = Material.objects.all()

    id_material = request.GET.get('id_material')
    name = request.GET.get('name')
    material_type = request.GET.get('material_type')
    status = request.GET.get('status')

    if id_material:
        material_list = material_list.filter(id_material__icontains=id_material)
    if name:
        material_list = material_list.filter(name__icontains=name)
    if material_type:
        try:
            material_type_obj = MaterialType.objects.get(name__iexact=material_type)
            material_list = material_list.filter(material_type=material_type_obj)
        except MaterialType.DoesNotExist:
            material_list = material_list.none() 
    if status:
        try:
            status_obj = Status.objects.get(name__iexact=status)
            material_list = material_list.filter(status=status_obj)
        except Status.DoesNotExist:
            material_list = material_list.none()

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="materials.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(['Material ID', 'Material Name', 'Material Type', 'Status', 'Created By', 'Created At', 'Updated At'])

        for material in material_list:
            writer.writerow([
                material.id_material, 
                material.name, 
                material.material_type, 
                material.status,
                material.created_by.username if material.created_by else 'N/A',
                material.create_at.strftime('%Y-%m-%d %H:%M:%S'),
                material.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            ])

        return response

    paginator = Paginator(material_list, 10)  # Show 10 materials per page  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        all_statuses = Status.objects.all().order_by('name')
    except NameError:
        all_statuses = []

    try:
        all_material_types = MaterialType.objects.all().order_by('name')
    except NameError:
        all_material_types = []

    context = {
        'page_obj': page_obj,
        'all_statuses': all_statuses,
        'all_material_types': all_material_types,

    }    

    return render(request, 'materials/material_list.html', context)

@login_required
def material_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials') # Redirect to materials if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.created_by = request.user
            material.save()

            return redirect('materials:material_create')
    else:
        form = MaterialForm()
        
    return render(request, 'materials/material_form.html', {'form': form})

@login_required
def material_edit(request, pk):

    material = get_object_or_404(Material, pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials') # Redirect to materials if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    material = Material.objects.get(pk=pk)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materials:material_list')
    else:
        form = MaterialForm(instance=material)

    context = {
        'form': form,
        'material': material,
    }

    return render(request, 'materials/material_form.html', context)

@login_required
def material_delete(request, pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('materials:material_list') # Redirect to materials if no permission
    
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        material.delete()
        return redirect('materials:material_list')
    
    return redirect('materials:material_list')

@login_required
def material_bulk_upload(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('materials:material_list')

    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)

        if form.is_valid():
            csv_file = request.FILES['csv_file']

            status_map = {
                status.name.strip().lower(): status 
                for status in Status.objects.all()
            }

            unit_map = {
                unit.name.strip().lower(): unit 
                for unit in Unit.objects.all()
            }

            unit_map.update({
                unit.abbreviation.strip().lower(): unit 
                for unit in Unit.objects.all()
            })

            material_type_map = {
                material_type.name.strip().lower(): material_type 
                for material_type in MaterialType.objects.all()
            }

            material_type_map.update({
                material_type.abbreviation.strip().lower(): material_type 
                for material_type in MaterialType.objects.all()
            })

            try:
                data_set = csv_file.read().decode('UTF-8')
            except UnicodeDecodeError:
                try:
                    csv_file.seek(0)  # Reset file pointer to the beginning
                    data_set = csv_file.read().decode('ISO-8859-1')
                except Exception as e:
                    messages.error(request, "Error occurred while reading the CSV file.")
                    return render(request, 'materials/material_bulk_upload.html', {'form': form})

            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)

            if reader.fieldnames:
                if reader.fieldnames[0].startswith('\ufeff'):
                    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

                cleaned_fieldnames = [key.strip() for key in reader.fieldnames]
                reader.fieldnames = cleaned_fieldnames

            successful_records = []
            error_records = []
            suppliers_to_create = []

            for i, row in enumerate(reader):
                row_number = i + 2
                form_data = {}

                for key, value in row.items():
                    cleaned_value = value.strip() if isinstance(value, str) else value
                    form_data[key] = cleaned_value

                unit_value = form_data.get('unit', '').strip().lower()
                unit_obj = unit_map.get(unit_value)
                if unit_obj:
                    form_data['unit'] = unit_obj.id
                else:
                    error_records.append({
                        'row': row_number,
                        'data': row,
                        'errors':{'unit': f'Unit "{unit_value}" does not exist.'}
                    })
                    continue

                material_type_value = form_data.get('material_type', '').strip().lower()
                material_type_obj = material_type_map.get(material_type_value)

                if material_type_obj:
                    form_data['material_type'] = material_type_obj.id
                else:
                    error_records.append({
                        'row': row_number,
                        'data': row,
                        'errors': {'material_type': f'Material Type "{material_type_value}" does not exist.'}
                    })
                    continue

                status_value = form_data.get('status', '').strip().lower()
                status_obj = status_map.get(status_value)

                if status_obj:
                    form_data['status'] = status_obj.pk
                else:
                    error_records.append({
                        'row': row_number,
                        'data': row,
                        'errors': {'status': f'Status "{status_value}" does not exist.'}
                    })
                    continue

                form = MaterialForm(form_data)

                if form.is_valid():
                    material = form.save(commit=False)
                    material.created_by = request.user
                    suppliers_to_create.append(material)
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

            if suppliers_to_create:
                Material.objects.bulk_create(suppliers_to_create)

            messages.success(request, f"Processed {len(successful_records)} materials created successfully.")

            context = {
                'form': form,
                'successful_count': len(successful_records),
                'error_count': len(error_records),
                'total_rows': len(successful_records) + len(error_records),
                'error_records': error_records,
                'successful_records': successful_records,
                'report_generated': True,
            }

            return render(request, 'materials/material_bulk_upload.html', context)

        return render(request, 'materials/material_bulk_upload.html', {'form': form})

    else:
        form = CsvUploadForm()
        return render(request, 'materials/material_bulk_upload.html', {'form': form})

@login_required
def download_template_materials(request):

    header_fields = ['id_material', 'name', 'description', 'unit_price', 'currency', 'category', 'supplier_id', 'stock_quantity', 'reorder_level', 'status']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="materials_template.csv"'

    writer = csv.writer(response)
    writer.writerow(header_fields)

    return response