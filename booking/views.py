from django.shortcuts import render
from .models import Booking


# Create your views here.
def booking_form(request):

    booking = Booking.objects.all().order_by('-date').first()
    return render(
        request,
        "booking/booking-page.html",
        {"booking": booking},
        )
