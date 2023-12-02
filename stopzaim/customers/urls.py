from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('customers_list', views.CustomerListView.as_view(), name='list'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),
    path('create_customer/', views.CustomerCreateView.as_view(), name="create_customer"),
    path('update_customer/<int:pk>/', views.CustomerUpdateView.as_view(), name="update_customer"),
    path('update_customer_tables/<int:pk>/<str:table>/', views.customer_formset_update, name="update_customer_tables"),
    path('companies_list', views.CompanyListView.as_view(), name='companies_list'),
    path('create_company/', views.CompanyCreateView.as_view(), name="create_company"),
    path('update_company/<int:pk>/', views.CompanyUpdateView.as_view(), name="update_company"),
    path('delete-company/<int:pk>/', views.delete_company, name='delete_company'),
]