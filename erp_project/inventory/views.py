from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import InventoryMovements
from .forms import InventoryMovementForm, CsvUploadForm
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
import io
from django.db import models
from users.models import UserRole
from django.contrib import messages

# Create your views here.
@login_required
def inventory_list(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__inventory'))['max_permission'] or 0

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission
    
    inventory_list = InventoryMovements.objects.all()

    id_inventory_movement = request.GET.get('id_inventory_movement')
    id_location = request.GET.get('id_location')
    id_material = request.GET.get('id_material')
    status = request.GET.get('status')
    quantity = request.GET.get('quantity')
    unit_type = request.GET.get('unit_type')
    movement_type = request.GET.get('movement_type')

    if id_inventory_movement:
        inventory_list = inventory_list.filter(id_inventory_movement__icontains=id_inventory_movement)
    if id_location:
        inventory_list = inventory_list.filter(id_location__icontains=id_location)
    if id_material:
        inventory_list = inventory_list.filter(id_material__icontains=id_material)
    if quantity:
        inventory_list = inventory_list.filter(quantity__icontains=quantity)
    if unit_type:
        inventory_list = inventory_list.filter(unit_type__icontains=unit_type)
    if movement_type:
        inventory_list = inventory_list.filter(movement_type__icontains=movement_type)
    

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

        response.write('\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(['Inventory Movement ID', 'Location ID', 'Material ID', 'Quantity', 'Unit Type', 'Movement Type'])

        for inventory_item in inventory_list:
            writer.writerow([
                inventory_item.id_inventory_movement,
                inventory_item.id_location,
                inventory_item.id_material,
                inventory_item.quantity,
                inventory_item.unit_type,
                inventory_item.movement_type,
            ])

        return response

    paginator = Paginator(inventory_list, 10)  # Show 10 inventory items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inventory_data = [
        [
            inventory_item.created_by.username if inventory_item.created_by else 'N/A',
            inventory_item.create_at.strftime('%Y-%m-%d %H:%M:%S'),
            inventory_item.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        ]
        for inventory_item in page_obj.object_list
    ]

    return response

    paginator = Paginator(inventory_list, 10)  # Show 10 inventory items per page
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
def inventory_create(request):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials') # Redirect to materials if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    if request.method == 'POST':
        form = InventoryMovementForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user
            inventory.save()

            return redirect('inventory:inventory_create')
    else:
        form = InventoryMovementForm()
        
    return render(request, 'inventory/inventory_form.html', {'form': form})

@login_required
def inventory_edit(request, pk):

    inventory = get_object_or_404(InventoryMovements, pk=pk)

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission == 1:
        return redirect('materials') # Redirect to materials if no permission

    if max_permission == 0:
        return redirect('dashboard') # Redirect to dashboard if no permission

    inventory = InventoryMovements.objects.get(pk=pk)

    if request.method == 'POST':
        form = InventoryMovementForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            return redirect('inventory:inventory_list')
    else:
        form = InventoryMovementForm(instance=inventory)

    context = {
        'form': form,
        'inventory': inventory,
    }

    return render(request, 'inventory/inventory_form.html', context)

@login_required
def inventory_delete(request, pk):

    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__materials'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('inventory:inventory_list') # Redirect to inventory if no permission
    
    inventory = get_object_or_404(InventoryMovements, pk=pk)

    if request.method == 'POST':
        inventory.delete()
        return redirect('inventory:inventory_list')
    
    return redirect('inventory:inventory_list')

@login_required
def inventory_bulk_upload(request):
    max_permission = UserRole.objects.filter(user_id=request.user).aggregate(max_permission=models.Max('role__inventory'))['max_permission'] or 0

    if max_permission < 2:
        return redirect('inventory:inventory_list')

    if request.method == 'POST':
        upload_form = CsvUploadForm(request.POST, request.FILES)

        if upload_form.is_valid():
            csv_file = request.FILES['csv_file']

            try:
                data_set = csv_file.read().decode('utf-8-sig')
            except UnicodeDecodeError:
                csv_file.seek(0)
                data_set = csv_file.read().decode('ISO-8859-1')

            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)
            required_fields = InventoryMovementForm.Meta.fields

            if not reader.fieldnames:
                messages.error(request, "The CSV file must contain a header row.")
                return render(request, 'inventory/inventory_bulk_upload.html', {'form': upload_form})

            reader.fieldnames = [name.strip() for name in reader.fieldnames]
            missing_fields = [name for name in required_fields if name not in reader.fieldnames]
            if missing_fields:
                messages.error(
                    request,
                    f"The CSV file is missing required columns: {', '.join(missing_fields)}.",
                )
                return render(request, 'inventory/inventory_bulk_upload.html', {'form': upload_form})

            successful_records = []
            error_records = []
            for i, row in enumerate(reader):
                row_number = i + 2
                form_data = {}

                for key, value in row.items():
                    if key is not None:
                        form_data[key] = value.strip() if isinstance(value, str) else value

                row_form = InventoryMovementForm(form_data)
                if row_form.is_valid():
                    inventory_movement = row_form.save(commit=False)
                    inventory_movement.created_by = request.user
                    inventory_movement.save()
                    successful_records.append({'row': row_number, 'data': form_data})
                else:
                    errors = {
                        field: ', '.join(error_list)
                        for field, error_list in row_form.errors.items()
                    }
                    error_records.append({
                        'row': row_number,
                        'data': form_data,
                        'errors': errors
                    })

            messages.success(
                request,
                f"Processed {len(successful_records)} inventory movements successfully.",
            )

            context = {
                'form': upload_form,
                'successful_count': len(successful_records),
                'error_count': len(error_records),
                'total_rows': len(successful_records) + len(error_records),
                'error_records': error_records,
                'successful_records': successful_records,
                'report_generated': True,
            }

            return render(request, 'inventory/inventory_bulk_upload.html', context)

        return render(request, 'inventory/inventory_bulk_upload.html', {'form': upload_form})

    else:
        upload_form = CsvUploadForm()
        return render(request, 'inventory/inventory_bulk_upload.html', {'form': upload_form})

@login_required
def download_template_inventory(request):

    header_fields = InventoryMovementForm.Meta.fields

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_template.csv"'

    writer = csv.writer(response)
    writer.writerow(header_fields)

    return response

