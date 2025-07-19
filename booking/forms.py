from django import forms
from .models import Booking
import datetime
from django.utils import timezone


class BookingForm(forms.ModelForm):
    """
    Form to allow users to make bookings
    """
    class Meta:
        """
        Model used and order of fields shown.
        """
        model = Booking
        fields = (
            'date',
            'time',
            'number_of_guests',
            'special_requests',
            'status')
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.HiddenInput(),
        }

    def clen_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError(
                'Date cannot be in the past')
        if date.weekday() == 0:
            raise forms.ValidationError(
                'Ups! We are closed on Mondays!')
        if date <= datetime.date.now():
            raise forms.ValidationError(
                'Ups! You have to book in advance!')
        return datetime
