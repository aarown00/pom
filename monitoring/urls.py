from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('<str:username>/create/', views.create_purchase_order, name='create'),
    path('<str:username>/dashboard/', views.dashboard_view, name='dashboard'),
    path('<str:username>/edit/<int:pk>', views.edit_purchase_order, name='edit'),
    path('<str:username>/itinenary/<int:pk>', views.edit_dws, name='itinenary'),
    path('<str:username>/cancel/<int:pk>', views.cancel_purchase_order, name='cancel'),

    path('<str:username>/create/customer', views.create_customer, name='create_customer'),
    path('<str:username>/dashboard/customer', views.dashboard_customer_view, name='dashboard_customer'), 
    path('<str:username>/delete/customer/<int:pk>', views.delete_customer, name='delete_customer'), 

    path('<str:username>/create/manpower', views.create_manpower, name='create_manpower'),  
    path('<str:username>/dashboard/manpower', views.dashboard_manpower_view, name='dashboard_manpower'), 
    path('<str:username>/delete/manpower/<int:pk>', views.delete_manpower, name='delete_manpower'), 

    # ajax
    path('ajax/validate-field/', views.ajax_validate_field, name='ajax_validate_field'),
    path('ajax/validate-time-total/', views.validate_time_total, name='ajax_validate_time_total'),

    #reports
    path('<str:username>/reports/', views.reports, name='reports'),
    path('<str:username>/reports/export/purchase_orders', views.export_po_to_excel, name='export_po_to_excel'),

]

handler404 = 'monitoring.views.custom_404_view'