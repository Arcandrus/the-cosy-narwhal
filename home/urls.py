from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("contact_success/", views.contact_success, name="contact_success"),
]
