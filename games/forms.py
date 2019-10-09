from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
  address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': '1234 Main St',
    'class': 'form-control'
  }), max_length=100 )
  optional_address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Apartment or suite',
    'class': 'form-control'
  }), label='Address 2 (Optional)', max_length=100, required=False )
  country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
    'class': 'custom-select d-block w-100'
  }))
  zip = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control'
  }))
  same_billing_address = forms.BooleanField(required=False)

  billing_address = forms.CharField(widget=forms.TextInput(attrs={
  'placeholder': '1234 Main St',
  'class': 'form-control'
  }), max_length=100, required=False )
  billing_optional_address = forms.CharField(widget=forms.TextInput(attrs={
    'placeholder': 'Apartment or suite',
    'class': 'form-control'
  }), label='Address 2 (Optional)', max_length=100, required=False )
  billing_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
    'class': 'custom-select d-block w-100'
  }), required=False)
  billing_zip = forms.CharField(widget=forms.TextInput(attrs={
    'class': 'form-control'
  }), required=False)


class CouponForm(forms.Form):
  code = forms.CharField(widget=forms.TextInput(attrs={
      'class': 'form-control',
      'placeholder': 'Promo code'
  }))
