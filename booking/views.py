from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Booking
from .forms import BookingForm
from bs4 import BeautifulSoup


# Create your views here.
def extract_modal_dialog(html):
    soup = BeautifulSoup(html, 'html.parser')
    modal = soup.select_one('.modal-dialog')
    return str(modal) if modal else '<div class="modal-dialog">Error loading modal.</div>'


def booking_page(request):
    """
    Display booking landing page
    """
    return render(request, 'booking/booking-page.html')


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
            booking.contact = request.user
            booking.save()
            return JsonResponse(
                {'success': True,
                 'message': 'Booking created successfully!'})
    else:
        form = BookingForm()

    # Only render the modal content section, not full HTML
    html = render_to_string('booking/booking-page.html', {
        'form': form,
        'modal_title': 'Make a New Booking',
        'modal_action': request.path,
        'modal_type': 'new_booking',
        'modal_show': True
    }, request=request)

    modal_html = extract_modal_dialog(html)
    return JsonResponse({'success': False, 'html': modal_html})


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


def modify_booking(request, pk):
    """
    Hadles update form for modal in booking-list.html
    """
    booking = get_object_or_404(Booking, pk=pk, contact=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {'success': True,
                 'message': 'Booking updated successfully!'})
    else:
        form = BookingForm(instance=booking)

    html = render_to_string('booking/booking-list.html', {
        'form': form,
        'modal_title': 'Update Booking',
        'modal_action': request.path,
        'modal_type': 'update',
        'modal_show': True
    }, request=request)

    modal_html = extract_modal_dialog(html)
    return JsonResponse({'success': False, 'html': modal_html})


def delete_booking(request, pk):
    """
    Handles delete confimation modal and form
    submission via AJAX.
    """
    booking = get_object_or_404(Booking, pk=pk, contact=request.user)

    if request.method == 'POST':
        booking.delete()
        return JsonResponse(
            {'success': True,
             'message': 'Booking deleted successfully!'})

    html = render_to_string('booking/booking-list.html', {
        'booking_to_delete': booking,
        'modal_title': 'Confirm Delete',
        'modal_action': request.path,
        'modal_type': 'delete',
        'modal_show': True
    }, request=request)

    modal_html = extract_modal_dialog(html)
    return JsonResponse({'success': False, 'html': modal_html})
