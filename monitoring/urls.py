from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('<str:username>/dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('create/', views.create_purchase_order, name='create'),
]