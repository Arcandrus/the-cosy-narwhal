from django import forms
from allauth.account.forms import SignupForm, LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from profiles.models import Profile


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Username or email',
            'class': 'form-control',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
            'autocomplete': 'current-password',
        })
        self.fields['remember'].widget.attrs.update({
            'class': 'form-check-input',
        })


class CustomSignupForm(SignupForm):
    full_name = forms.CharField(
        max_length=150,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Full Name"}),
    )
    street_address1 = forms.CharField(
        max_length=255,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Street Address 1"}),
    )
    street_address2 = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Street Address 2 (Optional)"}),
    )
    town_or_city = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Town or City"}),
    )
    county = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "County"}),
    )
    postcode = forms.CharField(
        max_length=20,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Postcode"}),
    )
    country = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Country"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Sign Up", css_class="btn btn-def"))

        # Set placeholders for built-in fields
        self.fields["username"].widget.attrs.update({"placeholder": "Username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )
        self.fields["password1"].help_text = """
            <div class="password-rules">
                Your password can't be too similar to your other personal information.
                <br>
                Your password must contain at least 8 characters.
                <br>
                Your password can't be a commonly used password.
                <br>
                Your password can't be entirely numeric.
            </div>
        """

        # Remove labels from all fields
        for field in self.fields.values():
            field.label = ""

    def save(self, request):
        user = super().save(request)

        # update profile fields as you already do
        profile = user.profile
        profile.full_name = self.cleaned_data['full_name']
        profile.street_address1 = self.cleaned_data['street_address1']
        profile.street_address2 = self.cleaned_data.get('street_address2', '')
        profile.town_or_city = self.cleaned_data['town_or_city']
        profile.county = self.cleaned_data['county']
        profile.postcode = self.cleaned_data['postcode']
        profile.country = self.cleaned_data['country']
        profile.save()

        return user
