from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from .models import Booking
from .forms import BookingForm


# Create your views here.

def booking_page(request):
    return render(request, 'booking/booking-page.html')


@login_required
def booking_form(request):
    """
    View to handle booking form submission.
    Used in the modal on 'booking-page.html'.
    """
    form = BookingForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status == 0
            booking.save()
            messages.success(
                request,
                'Booking submitted and awaiting approval!')
            return JsonResponse({'success': True})

    html = render_to_string('booking-page.html', {
        'form': form,
        'modal_type': 'new_booking',
        'modal_show': True,
        'modal_action': request.path,
        'modal_title': 'New Booking',
        'bookings': Booking.objects.filter(user=request.user).order_by('-date')
    }, request=request)
    return JsonResponse({'success': False, 'html': html})


@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/booking-list.html', {'bookings': bookings})


@login_required
def modify_booking(request, pk):
    """
    Allows a user to modify their existing booking.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    form = BookingForm(request.POST or None, instance=booking)
    if request.method == 'POST':
        if form.is_valid():
            form.status == 0
            form.save()
            messages.success(
                request,
                'Booking updated and awaiting approval')
            return JsonResponse(
                {'success': True})
    html = render_to_string('booking-list.html', {
        'form': form,
        'modal_type': 'update',
        'modal_show': True,
        'modal_action': request.path,
        'modal_title': 'Modify your Booking',
        'booking_to_update': booking,
        'bookings': Booking.objects.filter(user=request.user).order_by('-date')
    }, request=request)
    return JsonResponse({'success': False, 'html': html})


@login_required
def delete_booking(request, pk):
    """
    Allows looged-in users to cancel existing bookings
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(
            request,
            'Booking cancelled successfully!')
        return JsonResponse(
            {'success': True})
    html = render_to_string('booking-list.html', {
        'modal_type': 'delete',
        'modal_show': True,
        'modal_action': request.path,
        'booking_to_delete': booking,
        'bookings': Booking.objects.filter(user=request.user).order_by('-date')
    }, request=request)
    return JsonResponse({'success': False, 'html': html})
