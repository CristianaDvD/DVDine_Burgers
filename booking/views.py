from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Booking
from .forms import BookingForm


# Create your views here.
def booking_page(request):
    """
    Display booking landing page
    """
    return render(request, 'booking/booking-page.html')


@login_required
@require_http_methods(["GET", "POST"])
def booking_form(request):
    """
    View to handle booking form submission.
    Used in the modal on 'booking-page.html'
    with AJAX form.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 0
            booking.save()

            # Return full booking list page instead of JSON
            bookings = Booking.objects.filter(
                user=request.user).order_by('-date')
            return render(
                request,
                'booking/booking-list.html',
                {'bookings': bookings})
    else:
        form = BookingForm()

    return render(request, 'booking/modal-form.html', {
        'form': form,
        'modal_type': 'new_booking',
        'modal_title': 'New Booking',
        'modal_action': request.path,
    })


@login_required
def booking_list(request):
    """
    Display user's bookings in booking-list.html.
    Modals handled separately via AJAX
    """
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(
        request,
        'booking/booking-list.html',
        {'bookings': bookings})


@login_required
@require_http_methods(["GET", "POST"])
def modify_booking(request, pk):
    """
    Hadles update form for modal in booking-list.html
    """
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.user = request.user
            updated.status = 0
            updated.save()

            bookings = Booking.objects.filter(
                user=request.user).order_by('-date')
            return render(
                request,
                'booking/booking-list.html',
                {'bookings': bookings})
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/modal-form.html', {
        'form': form,
        'modal_type': 'update',
        'modal_title': 'Update Booking',
        'modal_action': request.path,
        'booking': booking,
    })


@login_required
@require_http_methods(["GET", "POST"])
def delete_booking(request, pk):
    """
    Handles delete confimation modal and form
    submission
    """
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()

        bookings = Booking.objects.filter(user=request.user).order_by('-date')
        return render(
            request,
            'booking/booking-list.html',
            {'bookings': bookings})

    return render(request, 'booking/modal-form.html', {
        'modal_type': 'delete',
        'modal_title': 'Confirm Delete Booking',
        'modal_action': request.path,
        'booking': booking,
    })
