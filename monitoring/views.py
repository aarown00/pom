from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect(f'/{request.user.username}/dashboard/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You have been successfully logged in, Welcome {user.username}!")
            return redirect(f'/{user.username}/dashboard/')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('login')
    return render(request, 'login.html')


@login_required
def dashboard_view(request, username):
    if request.user.username != username:
        return redirect(f'/{request.user.username}/dashboard/')
    return render(request, 'dashboard.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
