from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Create your views here.


def index(request):
    """Return index.html page"""
    return render(request, "home/index.html")


def faq(request):
    """Return faq.html page"""
    return render(request, "home/faq.html")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = f"New Contact Form Submission - {data['reason']}"
            message = f"""
            Name: {data['name']}
            Email: {data['email']}
            Reason: {data['reason']}
            Order Number: {data['order_number']}
            
            Message:
            {data['message']}
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['thecosynarwhal@outlook.com'], 
            )
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})

def contact_success(request):
    """Return contact_success.html page"""
    return render(request, "home/contact_success.html")
