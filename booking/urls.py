from django.urls import path
from . import views


urlpatterns = [
    path('', views.booking_page, name='bookingPage'),
    path('booking/', views.booking_list, name='bookingList'),
    path('booking/form/', views.booking_form, name='bookingForm'),
    path('booking/update/<int:pk>/',
         views.modify_booking, name='bookingUpdate'),
    path('booking/delete/<int:pk>/',
         views.delete_booking, name='bookingDelete'),
]
