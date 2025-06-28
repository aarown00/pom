from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PurchaseOrderForm
from .models import PurchaseOrder

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
def dashboard_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')

    purchase_orders = PurchaseOrder.objects.all().order_by('-id')

    return render(request, 'dashboard.html', {
        'purchase_orders': purchase_orders,
    })


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

def create_purchase_order(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Purchase order created successfully!')
            return redirect('create')  # change this to your list view name
    else:
        form = PurchaseOrderForm()
    return render(request, 'create_purchase_order.html', {'form': form})
