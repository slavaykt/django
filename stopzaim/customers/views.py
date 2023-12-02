from typing import Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from . import forms
from . import models
from django.urls import reverse

def get_customer_navs(title, is_new):
    navs = [
            {'title': 'Общие сведения', 'link': 'customers:update_customer' },
            {'title': 'Дети', 'link': 'customers:update_customer_tables', 'table': 'children'},
            {'title': 'Банковские счета', 'link': 'customers:update_customer_tables', 'table': 'bank_accounts'},
            {'title': 'Кредиторы', 'link': 'customers:update_customer_tables', 'table': 'payables'},
            {'title': 'Исполнительные документы', 'link': 'customers:update_customer_tables', 'table': 'executive_docs'},
            {'title': 'Обязательные платежи', 'link': 'customers:update_customer_tables', 'table': 'mandatory_payments'},
            {'title': 'Недвижимость', 'link': 'customers:update_customer_tables', 'table': 'realty'},
            {'title': 'Движимое имущество', 'link': 'customers:update_customer_tables', 'table': 'transports'}       
        ]
    for nav in navs:
        if (nav['title']==title):
            nav['active'] = True
            nav['disabled'] = True
        else:
            nav['active'] = False
            nav['disabled'] = is_new
    return navs

class CustomerListView(ListView):
    model = models.Customer
    template_name = 'customers/customer_list.html'
    context_object_name = 'customers'
    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['delete_url'] = 'customers:delete_customer'
        return ctx_data
    
def delete_customer(request, pk):
    try:
        obj = models.Customer.objects.get(id=pk)
    except obj.DoesNotExist:
        messages.success(
            request, 'Объект не существует'
            )
        return redirect('customers:list')

    obj.delete()
    messages.success(
            request, 'Строка удалена успешно'
            )
    return redirect('customers:list')   


class CustomerCreateView(CreateView):
    form_class = forms.CustomerForm
    model = models.Customer
    template_name = 'customers/customer_create.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect('customers:update_customer', pk=self.object.id)  

    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['customer'] = 0
        ctx_data['navs'] = get_customer_navs('Общие сведения',True)
        return ctx_data

class CustomerUpdateView(UpdateView):
    form_class = forms.CustomerForm
    model = models.Customer
    template_name = 'customers/customer_create.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.request.path_info)    

    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['customer'] = self.object
        ctx_data['navs'] = get_customer_navs('Общие сведения',False)
        return ctx_data

def customer_formset_update(request, pk, table):
    customer = models.Customer.objects.get(id=pk)
    if table=='children':
        formset_data = {
            'formset_model': forms.CustomerChildrenFormset,
            'formset_title': 'Дети',
            'formset_name': 'customerchild'} 
    elif table=='bank_accounts':
        formset_data = {
            'formset_model': forms.CustomerBankAccountFormset,
            'formset_title': 'Банковские счета',
            'formset_name': 'customerbankaccount'}
    elif table=='payables':
        formset_data = {
            'formset_model': forms.CustomerPayableFormset,
            'formset_title': 'Кредиторы',
            'formset_name': 'customerpayable'}
    elif table=='executive_docs':
        formset_data = {
            'formset_model': forms.CustomerExecutiveDocFormset,
            'formset_title': 'Исполнительные документы',
            'formset_name': 'customerexecutivedoc'}
    elif table=='mandatory_payments':
        formset_data = {
            'formset_model': forms.CustomerMandatoryPaymentFormset,
            'formset_title': 'Обязательные платежи',
            'formset_name': 'customermandatorypayment'}
    elif table=='realty':
        formset_data = {
            'formset_model': forms.CustomerRealtyFormSet,
            'formset_title': 'Недвижимость',
            'formset_name': 'customerrealty'}
    elif table=='transports':
        formset_data = {
            'formset_model': forms.CustomerTransportFormset,
            'formset_title': 'Движимое имущество',
            'formset_name': 'customertransport'}
    if request.method == 'POST':
        formset = formset_data['formset_model'](request.POST or None, instance=customer)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data.get('name', False))
                if form.cleaned_data.get('DELETE', False):
                    print('test')
            formset.save()
            return redirect(request.path_info)
    else:
        formset = formset_data['formset_model'](instance=customer)
    ctx_data = {'customer': customer,
                   'formset': formset,
                   'formset_name': formset_data['formset_name'],
                   'formset_title': formset_data['formset_title'],
                   'navs': get_customer_navs(formset_data['formset_title'],False)}
    return render(request,'customers/customer_formsets_create.html',ctx_data)    

class CompanyListView(ListView):
    model = models.Company
    template_name = 'customers/companies_list.html'
    context_object_name = 'companies'
    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['delete_url'] = 'customers:delete_company'
        return ctx_data

class CompanyCreateView(CreateView):
    form_class = forms.CompanyForm
    model = models.Company
    template_name = 'customers/company_create.html'


    def form_valid(self, form):
        self.object = form.save()
        return redirect('customers:update_company', pk=self.object.id)  

    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['company'] = 0
        return ctx_data
    
class CompanyUpdateView(UpdateView):
    form_class = forms.CompanyForm
    model = models.Company
    template_name = 'customers/company_create.html'

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.request.path_info)    

    def get_context_data(self, **kwargs):
        ctx_data = super().get_context_data(**kwargs)
        ctx_data['company'] = self.object
        return ctx_data
    
def delete_company(request, pk):
    try:
        obj = models.Company.objects.get(id=pk)
    except obj.DoesNotExist:
        messages.success(
            request, 'Объект не существует'
            )
        return redirect('customers:companies_list')

    obj.delete()
    messages.success(
            request, 'Строка удалена успешно'
            )
    return redirect('customers:companies_list')  