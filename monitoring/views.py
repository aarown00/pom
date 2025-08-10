from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm
from .forms_customer import CustomerDetailForm
from .forms_manpower import ManpowerDetailForm
from .forms_dws import DailyWorkStatusFormSet, DailyWorkStatusForm
from .models import PurchaseOrder, CustomerDetail, ManpowerDetail, DailyWorkStatus
from django.db.models import ProtectedError, Q
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from openpyxl import Workbook
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db import transaction


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect(f'/{request.user.username}/dashboard/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/{user.username}/dashboard/')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    return render(request, 'login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

User = get_user_model()

@login_required
def change_password(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')

    user = get_object_or_404(User, username=username)

    if request.method == "POST":
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save() 
            update_session_auth_hash(request, user)  
            messages.success(request, "Your password was successfully updated.")
            return redirect("dashboard", username=username)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = PasswordChangeForm(user)

    return render(request, "change_password.html", {"form": form, "username": username})

#purchase order---------------------------------------------------

@login_required
def dashboard_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')

    # Get filter values from GET request
    selected_status = request.GET.get('status')
    selected_customer = request.GET.get('customer')
    selected_started = request.GET.get('date_started')
    selected_target = request.GET.get('target_date')
    selected_completed = request.GET.get('completion_date')
    search_query = request.GET.get('search', '')

    queryset = PurchaseOrder.objects.all()

     # Count each status
    status_counts = {
        'pending': PurchaseOrder.objects.filter(status='Pending').count(),
        'ongoing': PurchaseOrder.objects.filter(status='Ongoing').count(),
        'completed': PurchaseOrder.objects.filter(status='Completed').count(),
        'cancelled': PurchaseOrder.objects.filter(status='Cancelled').count(),
        'delayed': PurchaseOrder.objects.exclude(status__in=[
            'Pending', 'Ongoing', 'Completed', 'Cancelled'
        ]).count(),
    }

    # Apply dropdown filters
    if selected_status:
        queryset = queryset.filter(status=selected_status)
    if selected_customer:
        queryset = queryset.filter(customer_branch__customer_name=selected_customer)
    if selected_started == "None":
        queryset = queryset.filter(date_started__isnull=True)
    elif selected_started:
        queryset = queryset.filter(date_started=selected_started)
    if selected_target:
        queryset = queryset.filter(target_date=selected_target)
    if selected_completed == "None":
        queryset = queryset.filter(completion_date__isnull=True)
    elif selected_completed:
        queryset = queryset.filter(completion_date=selected_completed)

    # Apply search filter last (AFTER other filters)
    if search_query:
        queryset = queryset.filter(purchase_order__icontains=search_query)    

    # Pagination
    paginator = Paginator(queryset.order_by('-id'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Distinct values for dropdowns
    customer_list = CustomerDetail.objects.order_by('customer_name').values_list('customer_name', flat=True).distinct()
    started_list = PurchaseOrder.objects.values_list('date_started', flat=True).distinct()
    target_list = PurchaseOrder.objects.values_list('target_date', flat=True).distinct()
    completed_list = PurchaseOrder.objects.values_list('completion_date', flat=True).distinct()

    po_numbers_list = PurchaseOrder.objects.values_list('purchase_order', flat=True).distinct()

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,

        'customer_list': customer_list,
        'started_list': started_list,
        'target_list': target_list,
        'completed_list': completed_list,
        'po_numbers_list': list(po_numbers_list),

        'selected_status': selected_status,
        'selected_customer': selected_customer,
        'selected_started': selected_started,
        'selected_target': selected_target,
        'selected_completed': selected_completed,
        'search_query': search_query,  

        'status_counts': status_counts,
    })


@login_required
def view_purchase_order(request, username, pk):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')

    po = get_object_or_404(PurchaseOrder, pk=pk)

    changes = []

    records = po.history.all().order_by('-history_date')

    for i in range(len(records) - 1):
        current = records[i]
        previous = records[i + 1]

        diff = {}
        for field in ['date_started', 'target_date', 'completion_date']:
            old_value = getattr(previous, field)
            new_value = getattr(current, field)
            if old_value != new_value:
                diff[field] = (old_value, new_value)

        if diff:
            changes.append({
                'user': current.history_user,
                'date': current.history_date,
                'diff': diff,
            })

    context = {
        'po': po,
        'changes': changes,
    }

    return render(request, 'view.html', context)


@login_required
def create_purchase_order(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/create/')

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase order created successfully!')
            return redirect('dashboard', username=request.user.username)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = PurchaseOrderForm()

    return render(request, 'create_purchase_order.html', {'form': form})

@login_required
def edit_purchase_order(request, username, pk):
    po_instance = get_object_or_404(PurchaseOrder, pk=pk)

    if po_instance.status == "Cancelled":
        messages.error(request, "This Purchase Order has been cancelled and cannot be updated.")
        return redirect('dashboard', username=username)

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=po_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase order updated successfully!')
            return redirect('edit', username=username, pk=pk)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = PurchaseOrderForm(instance=po_instance)

    return render(request, 'edit_purchase_order.html', {
        'form': form,
        'po': po_instance  # ✅ this line enables po.id to work in HTML
    })

@login_required
def cancel_purchase_order(request, username, pk):

    if not request.user.groups.filter(name="po_admin").exists():
        messages.error(request, "You do not have permission to cancel orders!")
        return redirect("dashboard", username=username)
    
    po = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == "POST" and request.POST.get("status") == "Cancelled":
        po.status = "Cancelled"
        po.save()
        messages.success(request, "Purchase Order has been cancelled.")
    else:
        messages.error(request, "Purchase Order already cancelled.")

    return redirect('dashboard', username=username)

#itinenary----------------------------------------------------------------------

@login_required
def edit_dws(request, username, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)

    if purchase_order.status == "Cancelled":
        messages.error(request, "This Purchase Order has been cancelled and cannot be updated.")
        return redirect('dashboard', username=username)

    if request.method == 'POST':
        formset = DailyWorkStatusFormSet(request.POST, instance=purchase_order)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Itinenary updated successfully!')
            return redirect('itinenary', username=username, pk=pk)
        else:
            messages.error(request, 'Missing or invalid fields!')
        
    else:
        formset = DailyWorkStatusFormSet(instance=purchase_order)

    return render(request, 'edit_dws.html', {
        'formset': formset,
        'po': purchase_order,
    })


@login_required
def dws(request, username, pk):
    
    if request.user.username != username: 
        return redirect('dashboard', username=request.user.username)
        
    po = get_object_or_404(PurchaseOrder, pk=pk)
    daily_work_statuses_list = po.daily_work_statuses.all().prefetch_related('manpower').order_by('id')

    paginator = Paginator(daily_work_statuses_list, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'po': po,
        'page_obj': page_obj, 
        'username': username,
    }

    return render(request, 'dws.html', context)


#customer----------------------------------------------------------------------


@login_required
def dashboard_customer_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/customer')

    search = request.GET.get('search', '').strip()
    
    qs = CustomerDetail.objects.all()
    
    if search:
        search_words = search.split()
        
        query_filter = Q()
        
        for word in search_words:
            word_filter = Q(customer_name__icontains=word) | Q(branch_name__icontains=word)
            query_filter &= word_filter
            
        qs = qs.filter(query_filter)

    qs = qs.order_by('customer_name')

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    customer_details = paginator.get_page(page_number)

    all_customers = CustomerDetail.objects.all().order_by('customer_name')

    return render(request, 'dashboard_customer.html', {
        'customer_details': customer_details,
        'search_query': search,
        'all_customers': all_customers, 
    })

@login_required
def delete_customer(request, username, pk):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/customer')

    if request.method == 'POST':
        customer = get_object_or_404(CustomerDetail, pk=pk)
        try:
            customer.delete()
            messages.success(request, "Customer deleted successfully.")
        except ProtectedError:
            messages.error(request, "Cannot delete this customer because it is still in use in existing P.O's!")

    return redirect('dashboard_customer', username=username)

@login_required
def create_customer(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/create/customer')

    if request.method == 'POST':
        form = CustomerDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer details created successfully!')
            return redirect('create_customer', username=request.user.username)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = CustomerDetailForm()

    return render(request, 'create_customer.html', {'form': form})

@login_required
def edit_customer(request, username, pk):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/edit/customer')

    customer = get_object_or_404(CustomerDetail, pk=pk)
    original_name = customer.customer_name  # before any changes

    if request.method == 'POST':
        form = CustomerDetailForm(request.POST, instance=customer)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_name = new_customer.customer_name

            with transaction.atomic():
                # Save the edited instance first
                new_customer.save()

                # If it was a case-only change (e.g., "KFC" -> "kfc"),
                # propagate that exact original string to all others that had the same exact casing.
                if original_name != new_name and original_name.lower() == new_name.lower():
                    # Update all other records whose customer_name exactly equals the old casing
                    CustomerDetail.objects.filter(customer_name=original_name).exclude(pk=new_customer.pk).update(customer_name=new_name)

            messages.success(request, 'Customer details updated successfully!')
            return redirect('edit_customer', username=request.user.username, pk=pk)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = CustomerDetailForm(instance=customer)

    return render(request, 'edit_customer.html', {
        'form': form,
        'customer': customer,
    })

#manpower----------------------------------------------------------------------

@login_required
def dashboard_manpower_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/manpower')

    search = request.GET.get('search', '').strip()

    qs = ManpowerDetail.objects.all()
    
    if search:
        search_words = search.split()
        query_filter = Q()
        
        for word in search_words:
            word_filter = Q(name__icontains=word) | Q(category__icontains=word)
            query_filter &= word_filter
            
        qs = qs.filter(query_filter)

    qs = qs.order_by('name')

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    manpower_details = paginator.get_page(page_number)
    
    # Get a separate queryset for the datalist, with all items
    all_manpower = ManpowerDetail.objects.all().order_by('name')

    return render(request, 'dashboard_manpower.html', {
        'manpower_details': manpower_details,
        'search_query': search,
        'all_manpower': all_manpower, # Pass all data for the datalist
    })


@login_required
def delete_manpower(request, username, pk):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/manpower')

    manpower = get_object_or_404(ManpowerDetail, pk=pk)

    try:
        manpower.delete()
        messages.success(request, "Manpower deleted successfully.")
    except ValidationError as e:
        messages.error(request, e.message)

    return redirect('dashboard_manpower', username=username)



@login_required
def create_manpower(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/create/manpower')

    if request.method == 'POST':
        form = ManpowerDetailForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manpower details created successfully!')
            return redirect('create_manpower', username=request.user.username)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = ManpowerDetailForm()

    return render(request, 'create_manpower.html', {'form': form})


@login_required
def edit_manpower(request, username, pk):
    if request.user.username != username:
        return redirect('edit_manpower', username=request.user.username, pk=pk)

    manpower = get_object_or_404(ManpowerDetail, pk=pk)

    if request.method == 'POST':
        form = ManpowerDetailForm(request.POST, instance=manpower)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manpower details updated successfully!')
            return redirect('edit_manpower', username=request.user.username, pk=pk)
        else:
            messages.error(request, 'Missing or invalid fields!')
    else:
        form = ManpowerDetailForm(instance=manpower)

    return render(request, 'edit_manpower.html', {'form': form, 'manpower': manpower})

#ajax
@csrf_exempt
def ajax_validate_field(request):
    if request.method == "POST":
        field_name = request.POST.get("field")
        value = request.POST.get("value")
        form_name = request.POST.get("form")  # now required
        instance_id = request.POST.get("id")

        data = {field_name: value}

        # Choose the correct form and model
        if form_name == "purchase_order":
            ModelForm = PurchaseOrderForm
            Model = PurchaseOrder
        elif form_name == "manpower":
            ModelForm = ManpowerDetailForm
            Model = ManpowerDetail
        elif form_name == "customer":
            ModelForm = CustomerDetailForm
            Model = CustomerDetail
        elif form_name == "dws":
            ModelForm = DailyWorkStatusForm
            Model = DailyWorkStatus
        else:
            return JsonResponse({"valid": False, "error": "Invalid form type."})

        # Editing support
        if instance_id:
            instance = Model.objects.get(pk=instance_id)
            form = ModelForm(data, instance=instance)
        else:
            form = ModelForm(data)

        form.is_valid()

        if form.errors.get(field_name):
            return JsonResponse({
                "valid": False,
                "error": form.errors[field_name][0]
            })
        else:
            return JsonResponse({"valid": True})

@require_POST
def validate_time_total(request):
    manpower_ids = request.POST.getlist('manpower[]')
    time_total = request.POST.get('time_total')

    if manpower_ids and not time_total:
        return JsonResponse({'valid': False, 'error': 'Time total is required when manpower is selected.'})

    return JsonResponse({'valid': True})


@login_required
def reports(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/reports')

    from_date_str = request.GET.get('from')
    to_date_str = request.GET.get('to')

    from_date = parse_date(from_date_str) if from_date_str else None
    to_date = parse_date(to_date_str) if to_date_str else None

    po_queryset = []
    if from_date and to_date:
        po_queryset = PurchaseOrder.objects.filter(
            date_recorded__range=(from_date, to_date)
        ).order_by('date_recorded')

    paginator = Paginator(po_queryset, 10) 
    page_number = request.GET.get('page')
    po_reports = paginator.get_page(page_number)

    return render(request, 'reports.html', {
        'username': username,
        'po_reports': po_reports,
        'from_date': from_date_str,
        'to_date': to_date_str,
    })


@login_required
def export_po_to_excel(request, username):
    # Parse the from and to dates from GET parameters
    from_date = parse_date(request.GET.get('from'))
    to_date = parse_date(request.GET.get('to'))

    # Format for filename
    from_date_str = from_date.strftime('%Y.%m.%d') if from_date else 'start'
    to_date_str = to_date.strftime('%Y.%m.%d') if to_date else 'end'

    filename = f"Purchase Order Report - {from_date_str} to {to_date_str}.xlsx"

    # Filter based on date range
    queryset = PurchaseOrder.objects.filter(date_recorded__range=(from_date, to_date))

    # Create Excel file
    wb = Workbook()
    ws = wb.active
    ws.title = "Purchase Orders"

    headers = [
        "Purchase Order", "Customer", "Branch/Address", "Classification", "Description", "Manpower Type",
        "Total Manpower", "Total Days", "Working Days", "Total Working Hours",
        "Recorded Date", "Received Date", "Started Date", "Target Date", "Completion Date",
        "COC No.", "DR No.", "Service Report No.", "Inv No.",
        "Remarks", "Status",

        
    ]
    ws.append(headers)

    for po in queryset:
        ws.append([
            po.purchase_order,
            po.customer_branch.customer_name,
            po.customer_branch.branch_name,
            po.classification,
            po.description,
            po.manpower_type if po.manpower_type else 'No manpower',

            po.manpower_total,
            po.total_days,
            po.working_days_total,
            po.work_hours_total,

            po.date_recorded.strftime('%Y-%m-%d'),
            po.purchase_order_received.strftime('%Y-%m-%d'),
            po.date_started.strftime('%Y-%m-%d') if po.date_started else 'None',
            po.target_date.strftime('%Y-%m-%d'),
            po.completion_date.strftime('%Y-%m-%d') if po.completion_date else 'None',

            po.coc_number if po.coc_number else 'None',
            po.dr_number if po.dr_number else 'None',
            po.service_report_number if po.service_report_number else 'None',
            po.invoice_number if po.invoice_number else 'None',

            po.remarks if po.completion_date else 'None',
            po.status,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

#logs
