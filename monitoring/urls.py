from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('<str:username>/create/', views.create_purchase_order, name='create'),
    path('<str:username>/dashboard/', views.dashboard_view, name='dashboard'),
    path('<str:username>/edit/<int:pk>', views.edit_purchase_order, name='edit'),
 
    
    path('<str:username>/create/customer', views.create_customer, name='create_customer'),
    path('<str:username>/create/customerlist', views.customerlist_view, name='customerlist'), 

    path('<str:username>/create/manpower', views.create_manpower, name='create_manpower'),  
    path('<str:username>/create/manpowerlist', views.manpowerlist_view, name='manpowerlist'), 


]