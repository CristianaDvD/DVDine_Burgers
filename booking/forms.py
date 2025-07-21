from django import forms
from .models import Booking
from django.utils import timezone
import datetime


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

    def clean_date(self):
        """
        raise error if time booked is in the past
        or if booking is made on Mondays
        """
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError(
                'Date cannot be in the past')
        if date.weekday() == 0:
            raise forms.ValidationError(
                'Ups! We are closed on Mondays!')
        return date

    def clean(self):
        """
        raise error if booking is made outside
        hours on Tue-Thus
        """
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            weekday = date.weekday()  # Monday = 0, Sunday = 6

            if 1 <= weekday <= 3:  # Tuesday to Thursday
                if not (datetime.time(12, 0) <= time <= datetime.time(21, 0)):
                    raise forms.ValidationError(
                        "Bookings on Tue–Thu are only allowed between 12:00 and 21:00."
                    )

        return cleaned_data
