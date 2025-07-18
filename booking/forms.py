from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Form to allow users to make bookings
    """
    class Meta:
        """
        Model used and order of fields shown.
        """
        model = Booking
        fields = ('date', 'time', 'number_of_guests', 'special_requests', 'status')
