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
            'care_details',
            'inventory',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'available_colors': forms.CheckboxSelectMultiple(), 
            'care_details': forms.Textarea(attrs={'rows': 2}),
        }