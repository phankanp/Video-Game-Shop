from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


class CheckoutForm(forms.Form):
    STATE_CHOICES = (("AL", "Alabama"), ("AK", "Alaska"), ("AZ", "Arizona"), ("AR", "Arkansas"), ("CA", "California"), ("CO", "Colorado"), ("CT", "Connecticut"), ("DE", "Delaware"), ("FL", "Florida"), ("GA", "Georgia"), ("HI", "Hawaii"), ("ID", "Idaho"), ("IL", "Illinois"), ("IN", "Indiana"), ("IA", "Iowa"), ("KS", "Kansas"), ("KY", "Kentucky"), ("LA", "Louisiana"), ("ME", "Maine"), ("MD", "Maryland"), ("MA", "Massachusetts"), ("MI", "Michigan"), ("MN", "Minnesota"), ("MS", "Mississippi"), ("MO", "Missouri"), ("MT",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    "Montana"), ("NE", "Nebraska"), ("NV", "Nevada"), ("NH", "New Hampshire"), ("NJ", "New Jersey"), ("NM", "New Mexico"), ("NY", "New York"), ("NC", "North Carolina"), ("ND", "North Dakota"), ("OH", "Ohio"), ("OK", "Oklahoma"), ("OR", "Oregon"), ("PA", "Pennsylvania"), ("RI", "Rhode Island"), ("SC", "South Carolina"), ("SD", "South Dakota"), ("TN", "Tennessee"), ("TX", "Texas"), ("UT", "Utah"), ("VT", "Vermont"), ("VA", "Virginia"), ("WA", "Washington"), ("WV", "West Virginia"), ("WI", "Wisconsin"), ("WY", "Wyoming"))

    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
        'id': 'address'
    }), max_length=100)
    optional_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control',
        'id': 'optional_address'
    }), label='Address 2 (Optional)', max_length=100, required=False)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id': 'country'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zip',
        'class': 'form-control',
        'id': 'zip'
    }))
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES, attrs={
        'class': 'custom-select d-block w-100',
        'id': 'state'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'form-control',
        'id': 'city'
    }))
    same_billing_address = forms.BooleanField(required=False)

    billing_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
        'id': 'billing_address'
    }), max_length=100, required=False)
    billing_optional_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control',
        'id': 'billing_optional_address'
    }), label='Address 2 (Optional)', max_length=100, required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id': 'billing_country'
    }), required=False)
    billing_zip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Zip',
        'class': 'form-control',
        'id': 'billing_zip'
    }), required=False)
    billing_state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES, attrs={
        'class': 'custom-select d-block w-100',
        'id': 'billing_state'
    }))
    billing_city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'form-control',
        'id': 'billing_city'
    }), required=False)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))
