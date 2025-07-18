from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm
from .forms_customer import CustomerDetailForm
from .forms_manpower import ManpowerDetailForm
from .forms_dws import DailyWorkStatusFormSet, DailyWorkStatusForm
from .models import PurchaseOrder, CustomerDetail, ManpowerDetail, DailyWorkStatus
from django.db.models import ProtectedError
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

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

#purchase order---------------------------------------------------

@login_required
def dashboard_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')

    purchase_orders = PurchaseOrder.objects.all().order_by('-id')

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

    return render(request, 'dashboard.html', {
        'purchase_orders': purchase_orders,
        'status_counts': status_counts,
    })

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
        form = PurchaseOrderForm()

    return render(request, 'create_purchase_order.html', {'form': form})

@login_required
def edit_purchase_order(request, username, pk):
    po_instance = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=po_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase order updated successfully!')
            return redirect('edit', username=username, pk=pk)
    else:
        form = PurchaseOrderForm(instance=po_instance)

    return render(request, 'edit_purchase_order.html', {
        'form': form,
        'po': po_instance  # ✅ this line enables po.id to work in HTML
    })

@login_required
def cancel_purchase_order(request, username, pk):
    po = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == "POST" and request.POST.get("status") == "Cancelled":
        po.status = "Cancelled"
        po.save()
        messages.success(request, "Purchase Order has been cancelled.")
    else:
        messages.error(request, "Invalid or missing status.")

    return redirect('dashboard', username=username)


@login_required
def edit_dws(request, username, pk):
    purchase_order = get_object_or_404(PurchaseOrder, pk=pk)

    if request.method == 'POST':
        formset = DailyWorkStatusFormSet(request.POST, instance=purchase_order)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Itinenary updated successfully!')
            return redirect('itinenary', username=username, pk=pk)
    else:
        formset = DailyWorkStatusFormSet(instance=purchase_order)

    return render(request, 'edit_dws.html', {
        'formset': formset,
        'po': purchase_order,
    })



#customer----------------------------------------------------------------------

@login_required
def dashboard_customer_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/customer')

    customer_details = CustomerDetail.objects.order_by('customer_name')

    return render(request, 'dashboard_customer.html', {
        'customer_details': customer_details,
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
        form = CustomerDetailForm()

    return render(request, 'create_customer.html', {'form': form})


#manpower----------------------------------------------------------------------

@login_required
def dashboard_manpower_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/manpower')

    manpower_details = ManpowerDetail.objects.order_by('name')

    return render(request, 'dashboard_manpower.html', {
        'manpower_details': manpower_details,
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
        form = ManpowerDetailForm()

    return render(request, 'create_manpower.html', {'form': form})



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
