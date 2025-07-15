from django import forms

REASON_CHOICES = [
    ('', 'Select a reason'),  # default empty option
    ('refund', 'Request Refund / Return'),
    ('problem', 'Problems With Order'),
    ('wisimo', 'Where Is My Order?'),
    ('custom', 'Custom Make'),
    ('other', 'Any Other'),
]

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    reason = forms.ChoiceField(
        required=True,
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    order_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Order Number'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message here...',
            'rows': 5
        })
    )