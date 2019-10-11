from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
  address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': '1234 Main St',
    'class': 'form-control',
    'id': 'address'
  }), max_length=100 )
  optional_address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Apartment or suite',
    'class': 'form-control',
    'id': 'optional_address'
  }), label='Address 2 (Optional)', max_length=100, required=False )
  country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
    'class': 'custom-select d-block w-100',
    'id': 'country'
  }))
  zip = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'id': 'zip'
  }))
  same_billing_address = forms.BooleanField(required=False)

  billing_address = forms.CharField(widget=forms.TextInput(attrs={
  'placeholder': '1234 Main St',
  'class': 'form-control',
    'id': 'billing_address'
  }), max_length=100, required=False )
  billing_optional_address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Apartment or suite',
    'class': 'form-control',
    'id': 'billing_optional_address'
  }), label='Address 2 (Optional)', max_length=100, required=False )
  billing_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
    'class': 'custom-select d-block w-100',
    'id': 'billing_country'
  }), required=False)
  billing_zip = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control',
    'id': 'billing_zip'
  }), required=False)


class CouponForm(forms.Form):
  code = forms.CharField(widget=forms.TextInput(attrs={
      'class': 'form-control',
      'placeholder': 'Promo code'
  }))