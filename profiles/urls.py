from django.urls import path
from .views import profile_view
from . import views

urlpatterns = [
    path('', profile_view, name='profile'),
]