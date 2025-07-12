import datetime
from django.db import models
from django.contrib.auth.models import User

# Defines time options for bookings (12:00 to 23:00)
TIMES = tuple()
time_list = list(TIMES)
for hrs in range(12, 23):
    for min in range(0, 60, 15):
        if min == 0:
            time_text = f'{hrs}:00'
        else:
            time_text = f'{hrs}:{min}'

        time_value = datetime.time(hrs, min)
        time_list.append((time_value, time_text))

TIMES = tuple(time_list)

# Defines number of guest range available for bookings min=1, max=12.
GUEST_NUMBER = tuple()
for num in range(1, 13):
    GUEST_NUMBER = ((num, str(num)),)

# Variable to allow admin to control bookings
STATUS = (
    (0, 'Pending'),
    (1, 'Confirmed'),
    (2, 'Cancelled'),
    (3, 'Rejected'),
)


# Create your models here.
class Booking(models.Model):
    """
    Creates the model for restaurant to manage bookings
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="bookings")
    date = models.DateField()
    time = models.TimeField(choices=TIMES)
    number_of_guests = models.PositiveIntegerField(choices=GUEST_NUMBER,
                                                   default=2)
    status = models.IntegerField(choices=STATUS, default=0)
    special_requests = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        status_display = dict(STATUS)[self.status]
        return f"Booking for {self.user} on {self.date} at {self.time} is {status_display}."
