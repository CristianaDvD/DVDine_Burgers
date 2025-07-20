from django.urls import path
from . import views


urlpatterns = [
    path('', views.booking_page, name='bookingPage'),
    path('list/', views.booking_list, name='bookingList'),
    path('create/', views.booking_form, name='bookingForm'),
    path('update/<int:pk>/',
         views.modify_booking, name='bookingUpdate'),
    path('delete/<int:pk>/',
         views.delete_booking, name='bookingDelete'),
]
