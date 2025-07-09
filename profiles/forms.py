from django import forms
from .models import Profile

class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name',
            'street_address1',
            'street_address2',
            'town_or_city',
            'county',
            'postcode',
            'country',
        ]
        # Keep placeholders for better UX
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
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            # Add form-control class
            existing_classes = field.widget.attrs.get('class', '')
            classes = (existing_classes + ' form-control').strip()
            field.widget.attrs['class'] = classes

            # Remove labels by setting label to empty string
            field.label = ''
