from django.contrib import admin
from .models import Booking
from django_summernote.admin import SummernoteModelAdmin


class BookingAdmin(admin.ModelAdmin):
    """
    Creates bookings list for admin to see and search.
    """
    list_display = ('user', 'date', 'time', 'number_of_guests', 'special_requests', 'status')
    list_filter = ('date', 'time', 'status')
    search_fields = ('status', 'date')


# Register your models here.
admin.site.register(Booking)
