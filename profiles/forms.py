from django import forms
from .models import Profile

class DeliveryInfoForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,  # Not required since it won't be edited here
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control',
        }),
        label='',
    )

    class Meta:
        model = Profile
        fields = [
            'full_name',
            # we won't include email here because it's a separate field
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'street_address1': forms.TextInput(attrs={'placeholder': 'Street Address 1'}),
            'street_address2': forms.TextInput(attrs={'placeholder': 'Street Address 2'}),
            'town_or_city': forms.TextInput(attrs={'placeholder': 'Town or City'}),
            'county': forms.TextInput(attrs={'placeholder': 'County'}),
            'postcode': forms.TextInput(attrs={'placeholder': 'Postcode'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)
        super().__init__(*args, **kwargs)

        # Set the email field value to user email and keep it disabled
        if user_email:
            self.fields['email'].initial = user_email

        for field_name, field in self.fields.items():
            # form-control class for all except email (already set in widget attrs)
            if field_name != 'email':
                existing_classes = field.widget.attrs.get('class', '')
                classes = (existing_classes + ' form-control').strip()
                field.widget.attrs['class'] = classes
            field.label = ''

            field_order = [
                'full_name',
                'email',
                'street_address1',
                'street_address2',
                'town_or_city',
                'county',
                'postcode',
                'country',
            ]
            self.fields = {k: self.fields[k] for k in field_order if k in self.fields}

