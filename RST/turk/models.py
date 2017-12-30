from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator


# 25 stations
class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=250)

    def __str__(self):
        return self.station_name


# 28 trains total
# 16 trains M-F
# 12 trains Sat and sun
# directions is 50/50
# train_direction: 1 = Bostons 0 = Washington
# train_days: 1 = weekend, 0 = weekdays
class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    train_start = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_start')
    train_end = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='train_end')
    train_direction = models.BooleanField(default=0)
    train_days = models.BooleanField(default=1)

    def __str__(self):
        dir = ''
        day = ''
        if self.train_direction == 1:
            dir = "Boston"
        else:
            dir = 'Washigton'
        if self.train_days == 1:
            day = 'weekend'
        else:
            day = 'weekday'
        return "To " + dir + " " + day

# every train has 25 stops
class Stop(models.Model):
    stop_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    time_in = models.TimeField(default=datetime.now)
    time_out = models.TimeField(default=datetime.now)

    def __str__(self):
        return self.train.__str__() + " stops at " + self.station.__str__() + " at " + str(self.time_in)


class Passenger(models.Model):
    passenger_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=250)
    lname = models.CharField(max_length=250)
    billing_address = models.CharField(max_length=250)
    #preferred_card_number = models.IntegerField(validators=[MinValueValidator(1000000000000000), MaxValueValidator(9999999999999999)], default=9999999999999999)

    def __str__(self):
        return str(self.fname)

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    paying_passenger_id = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    reservation_date = models.DateField(default=datetime.today)

    def __str__(self):
        return self.paying_passenger_id.fname+"'s reservation"


# segment north/south integer referes to the station id
# 24 total segments
class Segment(models.Model):
    segment_id = models.AutoField(primary_key=True)
    segment_north = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='seg_n')
    segment_south = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='seg_s')
    seg_fare = models.FloatField(default=0)

    def __str__(self):
        return self.segment_north.station_name + " to " + self.segment_south.station_name


# total 448 seats per train
class Seats_Free(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    seat_free_date = models.DateField(default=datetime.today)
    free_seat = models.IntegerField(default=448)

    def __str__(self):
        return self.train.__str__() + " seat: " + str(self.free_seat)


# May need Trips Model, for now, dont see reason why we need it
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    trip_start = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='trip_start')
    trip_end = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='trip_end')
    fare = models.FloatField(default=0)
    trip_date = models.DateField(default=datetime.today)










