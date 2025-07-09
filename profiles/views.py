from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from checkout.models import Order
from django.contrib import messages

@login_required
def profile_view(request):
    profile = request.user.profile  # Assumes a Profile instance exists
    past_orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        # Update profile with submitted form data
        profile.full_name = request.POST.get('full_name', profile.full_name)
        profile.street_address1 = request.POST.get('street_address1', profile.street_address1)
        profile.street_address2 = request.POST.get('street_address2', profile.street_address2)
        profile.town_or_city = request.POST.get('town_or_city', profile.town_or_city)
        profile.county = request.POST.get('county', profile.county)
        profile.postcode = request.POST.get('postcode', profile.postcode)
        profile.country = request.POST.get('country', profile.country)
        profile.save()

        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')  # Reload page after saving

    context = {
        'profile': profile,
        'past_orders': past_orders,
    }
    return render(request, 'profiles/profile.html', context)