from django import forms
from .models import Product, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.RadioSelect(
            choices=[(i, str(i)) for i in range(1, 6)],
        )
        self.fields['rating'].label = 'Rating'

from django import forms
from .models import Product  # Adjust import as needed

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'code',
            'name',
            'description',
            'size',
            'has_colors',
            'color',
            'available_colors',
            'price',
            'image',
            'image_url',
            'inventory',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'available_colors': forms.CheckboxSelectMultiple(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Skip adding form-control for checkbox/radio groups
            if isinstance(field.widget, (forms.CheckboxSelectMultiple, forms.CheckboxInput, forms.RadioSelect)):
                continue
            # Add 'form-control' class
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
