from django import forms
from . import models

common_input_class = 'form-control mb-2'
text_widget = forms.TextInput(attrs={'class': common_input_class})
select_widget = forms.Select(attrs={'class': common_input_class})
date_widget = forms.DateInput(attrs={'class': common_input_class,'type': 'date'})
number_widget = forms.NumberInput(attrs={'class':'form-control'})
text_area_widget = forms.Textarea(attrs={'class': common_input_class})
checkbox_widget = forms.CheckboxInput(attrs={'class': 'form-check-input'})

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        exclude = []
        widgets = {
            'first_name': text_widget,
            'middle_name': text_widget,
            'surname': text_widget,
            'gender': select_widget,
            'birthdate': date_widget,
            'phone': text_widget,
            'tax_id': text_widget,
            'snils': text_widget,
            'passport_series': text_widget,
            'passport_number': text_widget,
            'passport_issuer': text_widget,
            'passport_issue_date': date_widget,
            'passport_issuer_code': text_widget,
            'address': text_widget,
            'birthplace': text_widget,
            'tax_inspection': select_widget,
            'occupation': select_widget,
            'previous_year_income': text_widget,
            'job': select_widget,
            'position': text_widget,
            'sro': select_widget,
            'arbitration_court': select_widget,
            'gosuslugi': text_widget,
            'application_date': date_widget,
            'comments': text_area_widget,
            'is_married': checkbox_widget,
            'spouse_name': text_widget
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.required = False
                field.widget.attrs['required'] = False

class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        fields = ['name']
        widgets = {
            'name': text_widget
        }

class CustomerLoanForm(forms.ModelForm):
    class Meta:
        model = models.CustomerLoan
        exclude = []
        widgets = {
            'company': select_widget,
            'amount': number_widget
        }

CustomerLoansFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerLoan, form=CustomerLoanForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerChildForm(forms.ModelForm):
    class Meta:
        model = models.CustomerChild
        exclude = []
        widgets = {
            'name': text_widget,
            'gender': select_widget,
            'birthdate': date_widget, 
        }

CustomerChildrenFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerChild, form=CustomerChildForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerBankAccountForm(forms.ModelForm):
    class Meta:
        model = models.CustomerBankAccount
        exclude = []
        widgets = {
            'type': select_widget,
            'currency': select_widget,
            'account_number': text_widget,
            'bank': select_widget,
            'balance': number_widget,
            'opening_date': date_widget
        }          

CustomerBankAccountFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerBankAccount, form=CustomerBankAccountForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerPayableForm(forms.ModelForm):
    class Meta:
        model = models.CustomerPayable
        exclude = []
        widgets = {
            'type': select_widget,
            'lender': select_widget,
            'account_number': text_widget,
            'basis': text_widget,
            'gross_amount': number_widget,
            'net_amount': number_widget,
            'penalties_amount': number_widget,
        }          

CustomerPayableFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerPayable, form=CustomerPayableForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerExecutiveDocForm(forms.ModelForm):
    class Meta:
        model = models.CustomerExecutiveDoc
        exclude = []
        widgets = {
            'type': select_widget,
            'date': date_widget,
            'doc_number': text_widget,
            'executor': text_widget,
            'content': text_widget,
        }          

CustomerExecutiveDocFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerExecutiveDoc, form=CustomerExecutiveDocForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerMandatoryPaymentForm(forms.ModelForm):
    class Meta:
        model = models.CustomerMandatoryPayment
        exclude = []
        widgets = {
            'tax_name': select_widget,
            'arrears_amount': number_widget,
            'penalties_amount': number_widget
        }          

CustomerMandatoryPaymentFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerMandatoryPayment, form=CustomerMandatoryPaymentForm,
    extra=0, can_delete=True, can_delete_extra = True 
)

class CustomerRealtyForm(forms.ModelForm):
    class Meta:
        model = models.CustomerRealty
        exclude = []
        widgets = {
            'name': text_widget,
            'type': select_widget,
            'property_type': select_widget,
            'area': number_widget,
            'acquiring_basis': text_widget,
            'pledge': text_widget,
            'address': text_widget,
        }

CustomerRealtyFormSet = forms.inlineformset_factory(
    models.Customer, models.CustomerRealty, form=CustomerRealtyForm,
    extra=0, can_delete=True, can_delete_extra = True
)

class CustomerTransportForm(forms.ModelForm):
    class Meta:
        model = models.CustomerTransport
        exclude = []
        widgets = {
            'name': text_widget,
            'type': select_widget,
            'property_type': select_widget,
            'cost': number_widget,
            'production_year': text_widget,
            'plate_number': text_widget,
            'pledge': text_widget,
            'address': text_widget,
        }        

CustomerTransportFormset = forms.inlineformset_factory(
    models.Customer, models.CustomerTransport, form=CustomerTransportForm,
    extra=0, can_delete=True, can_delete_extra = True 
)