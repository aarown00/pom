from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm
from .forms_customer import CustomerDetailForm
from .forms_manpower import ManpowerDetailForm
from .models import PurchaseOrder, CustomerDetail, ManpowerDetail

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
            return redirect('dashboard', username=username)
    else:
        form = PurchaseOrderForm(instance=po_instance)

    return render(request, 'edit_purchase_order.html', {
        'form': form,
        'po': po_instance  # ✅ this line enables po.id to work in HTML
    })


#customer----------------------------------------------------------------------

@login_required
def customerlist_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/create/customerlist')

    customer_details = CustomerDetail.objects.order_by('customer_name')

    return render(request, 'dashboard_customer.html', {
        'customer_details': customer_details,
    })

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
def manpowerlist_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/create/manpowerlist')

    manpower_details = ManpowerDetail.objects.order_by('name')

    return render(request, 'dashboard_manpower.html', {
        'manpower_details': manpower_details,
    })


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