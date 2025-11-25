from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Booking
from .forms import BookingForm


# Create your views here.
def booking_page(request):
    """
    Display booking landing page
    """
    return render(request, 'booking/booking-page.html')


def custom_permission_denied(request, exception=None):
    """
    Custom 403 handler
    """
    return render(request, "403.html", status=403)


def get_booking_or_raise(user, pk):
    """
    Fetch a booking by PK.
    Raises Http404 if it does not exist.
    Raises PermissionDenied if it exists but is not owned by `user`.
    """
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist.")

    if booking.user != user:
        raise PermissionDenied("You do not have permission to access this booking.")

    return booking


@login_required
def booking_list(request):
    """
    Display only logged-in user's bookings in booking-list.html.
    Any attemp to pass a different user ID will be forbidden.
    Modals handled separately via AJAX.
    """
    if "user" in request.GET:
        if request.GET["user"] != str(request.user.id):
            raise PermissionDenied("You cannot view another user's bookings.")

    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(
        request,
        'booking/booking-list.html',
        {'bookings': bookings})


@login_required
@require_http_methods(["GET", "POST"])
def booking_form(request):
    """
    Handle booking creation via modal form.
    """
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 0
            booking.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                # return just the modal, JS will reload page
                return render(request, 'booking/modal-form.html', {
                    'form': BookingForm(),
                    'modal_type': 'new_booking',
                    'modal_title': 'New Booking',
                    'modal_action': request.path,
                })

            return redirect('bookingList')
    else:
        form = BookingForm()

    return render(request, 'booking/modal-form.html', {
        'form': form,
        'modal_type': 'new_booking',
        'modal_title': 'New Booking',
        'modal_action': request.path,
    })


@login_required
@require_http_methods(["GET", "POST"])
def modify_booking(request, pk):
    """
    Handle booking update via modal.
    Deny access if not owner's bookings.
    """
    booking = get_booking_or_raise(request.user, pk)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.user = request.user
            updated.status = 0
            updated.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return render(request, 'booking/modal-form.html', {
                    'form': BookingForm(instance=updated),
                    'modal_type': 'update',
                    'modal_title': 'Update Booking',
                    'modal_action': request.path,
                    'booking': updated,
                })

            return redirect('bookingList')
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
    Handle delete confirmation via modal.
    Deny access if not owner's bookings.
    """
    booking = get_booking_or_raise(request.user, pk)

    if request.method == 'POST':
        booking.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            # JS will reload page
            return render(request, 'booking/modal-form.html', {
                'modal_type': 'delete',
                'modal_title': 'Confirm Delete Booking',
                'modal_action': request.path,
            })
        return redirect('bookingList')

    return render(request, 'booking/modal-form.html', {
        'modal_type': 'delete',
        'modal_title': 'Confirm Delete Booking',
        'modal_action': request.path,
        'booking': booking,
    })
