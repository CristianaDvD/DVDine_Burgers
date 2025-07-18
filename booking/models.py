import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


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
    number_of_guests = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    status = models.IntegerField(choices=STATUS, default=0)
    special_requests = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        status_display = dict(STATUS)[self.status]
        return f"Booking for {self.user} on {self.date} at {self.time} is {status_display}."
