from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from .forms import *
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone
from datetime import datetime

#url - views - html

from .models import *
import csv


# train_direction: 1 = Bostons 0 = Washington
# train_days: 1 = weekend, 0 = weekdays
# bigger = washington
def front_page(request):

    #testing:
    print("Testing here")
    train = Stop.objects.filter(pk=1)
    print(Stop.train)
    print("Testing done")

    #sf = Seats_Free.objects.filter(train=get_object_or_404(Train, pk=28))


    all_stations = Station.objects.all()

    form = SeatfreeForm(request.POST or None)

    try:
        if request.method == 'POST':
            day = request.POST.get('day')
            station_id = request.POST.get('station')
            destination_station_id = request.POST.get('destination')

            date = form.save(commit=False)
            date = date.seat_free_date
            print("date: ",type(date))
            print(day," ",train)

            t_day = 1
            t_dir = 1

            if day == "weekday":
                t_day = 0
            if int(destination_station_id) > int(station_id):
                t_dir = 0
                print("Goint to washington!!")

            print(type(station_id),station_id)

            #all_trains = Train.objects.filter(train_direction=t_dir, train_days=t_day, stop__station=get_object_or_404(Station, pk=station_id))
            all_trains = Train.objects.filter(train_direction=t_dir, train_days=t_day,
                                              stop__station=get_object_or_404(Station, pk=station_id),
                                              seats_free__segment=station_id,
                                              seats_free__seat_free_date=date,
                                              seats_free__free_seat__gte=1)
            #Cannot resolve keyword 'seat_free' into field. Choices are: seats_free, stop, train_days,
            #  train_direction, train_end, train_end_id, train_id, train_start, train_start_id

            all_stops = Stop.objects.filter(train__in=all_trains, station=get_object_or_404(Station, pk=station_id))
            all_seats_free = Seats_Free.objects.filter(train__in=all_trains,
                                                       segment=get_object_or_404(Segment, pk=station_id),
                                                       seat_free_date=date,
                                                       free_seat__gte=1)

            context = {
                'all_trains': all_trains,
                'all_stations': all_stations,
                'segment_id': station_id,
                'destination_station_id': destination_station_id,
                'date': date,
                'all_stops': all_stops,
                'all_seats_free': all_seats_free,
                'form': form,
            }
            return render(request, 'turk/front_page.html', context)
    except ValueError:
        pass
    context = {
        'all_trains': None,
        'all_stations': all_stations,
        'segment_id': None,
        'destination_station_id': None,
        'date': None,
        'all_stops': None,
        'all_seats_free': None,
        'form': form,
    }
    return render(request, 'turk/front_page.html', context)


# TODO: need to calculate fare
def reservation(request, stop_id, train_id, seg_id, des_id, date):
    form = PassengerForm(request.POST or None)

    stop = get_object_or_404(Stop, pk=stop_id)
    train = get_object_or_404(Train, pk=train_id)
    segment = get_object_or_404(Segment, pk=seg_id)
    start = get_object_or_404(Station,pk=seg_id)
    des = get_object_or_404(Station, pk=des_id)
    sf = get_object_or_404(Seats_Free, train=train, segment=segment, seat_free_date=date)
    #sf = Seats_Free.objects.filter(train=train, segment=segment)
    sf.free_seat -= 1
    sf.save()
    print("Free seat left: ", sf.free_seat)

    total_fare = 0

    seg_id = int(seg_id)
    des_id = int(des_id)

    big_val = 0
    small_val = 0

    if seg_id > des_id:
        big_val += seg_id
        small_val += des_id
    else:
        big_val += des_id
        small_val += seg_id

    print('seg id: ', seg_id)
    print('des if: ', des_id)
    print('big val: ', big_val)
    print('small val: ', small_val)

    for i in range(small_val,big_val):
        seg = get_object_or_404(Segment, pk=i)
        total_fare += seg.seg_fare

    print("Total Fare:", total_fare)

    if form.is_valid():
        passenger = form.save(commit=False)
        passenger.save()
        res = Reservation(paying_passenger_id=passenger, reservation_date=date)
        res.save()
        trip = Trip(reservation=res, trip_start=start, trip_end=des, fare=total_fare, trip_date=date)
        trip.save()

        context = {
            'passenger_id': passenger.passenger_id,
            'reservation_id': res.reservation_id,
            'stop': stop,
            'form': form,
        }
        print("Confirm Res")
        #return render(request, 'turk/confirm_cancellation.html')
        return redirect('turk:confirm_reservation', pass_id=passenger.passenger_id,
                        res_id=res.reservation_id, stop_id=stop_id, trip_id=trip.trip_id)

    context = {
        'passenger_id': None,
        'reservation_id': None,
        'stop': None,
        'form': form,
    }

    return render(request, 'turk/reservation.html',context)


def confirm_reservation(request, pass_id, res_id, stop_id, trip_id):
    passenger = get_object_or_404(Passenger, pk=pass_id)
    reservation = get_object_or_404(Reservation, pk=res_id)
    stop = get_object_or_404(Stop, pk=stop_id)
    trip = get_object_or_404(Trip, pk=trip_id)

    context = {
        'passenger_id':passenger.passenger_id,
        'reservation_id':reservation.reservation_id,
        'trip': trip,
        'stop':stop
    }

    return render(request, 'turk/confirm_reservation.html', context)

# Also has rebook functionality
def cancellation(request):
    context = {
        'error': 0,
    }

    if request.method == 'POST':
        pass_id = request.POST.get('passenger')
        res_id = request.POST.get('reservation')
        reason = request.POST.get('reason')

        try:
            passenger = Passenger.objects.get(pk=pass_id)
            reservation = Reservation.objects.get(pk=res_id)
            print("pass: ", pass_id)
            print("res: ", res_id)
            print("reason: ", reason)

            if reason == "cancel":
                passenger.delete()
                return redirect('turk:confirm_cancellation')
            else:
                passenger.delete()
                return redirect('turk:front_page')
        except ObjectDoesNotExist:
            context = {
                'error': 1,
            }
            print("No such passenger")
            return render(request, 'turk/cancellation.html',context)

    return render(request, 'turk/cancellation.html',context)


def confirm_cancellation(request):
    return render(request, 'turk/confirm_cancellation.html')


# TODO: fill in models here
def createdb(request):

    print("Creating db")

    Station.objects.all().delete()
    Train.objects.all().delete()
    Stop.objects.all().delete()
    Passenger.objects.all().delete()
    Reservation.objects.all().delete()
    Segment.objects.all().delete()
    Seats_Free.objects.all().delete()

    f = open('turk/railroad1_stations.csv','r');
    reader = csv.reader(f)
    for row in reader:
        station = Station(station_id = row[0], station_name = row[1])
        station.save()
    f.close()

    f = open('turk/railroad1_trains.csv','r')
    reader = csv.reader(f)
    for row in reader:
        train = Train(train_id=row[0],train_start=get_object_or_404(Station, pk=row[1]),train_end=get_object_or_404(Station, pk=row[2]),train_direction=row[3],train_days=row[4])
        train.save()
    f.close()

    f = open('turk/railroad1_stops_at.csv','r')
    reader = csv.reader(f)
    for row in reader:
        stop = Stop(train=get_object_or_404(Train, pk=row[0]),station = get_object_or_404(Station, pk=row[1]),time_in = row[2],time_out = row[3])
        stop.save()
    f.close()

    f = open('turk/railroad1_passengers.csv','r')
    reader = csv.reader(f)
    for row in reader:
        passenger = Passenger(passenger_id=row[0],fname=row[1],lname=row[2],billing_address=row[6])
        passenger.save()
    f.close()

    f = open('turk/railroad1_reservations.csv','r')
    reader = csv.reader(f)
    for row in reader:
        reservation = Reservation(reservation_id=row[0],paying_passenger_id=row[2],reservation_date=row[1])
        reservation.save()
    f.close()

    f = open('turk/railroad1_segments.csv','r')
    reader = csv.reader(f)
    for row in reader:
        segment = Segment(segment_id=row[0],segment_north=get_object_or_404(Station, pk=row[1]),segment_south=get_object_or_404(Station, pk=row[2]),seg_fare=row[3])
        segment.save()
    f.close()

    f = open('turk/railroad1_seats_free.csv','r')
    reader = csv.reader(f)
    for row in reader:
        sf = Seats_Free(train=get_object_or_404(Train, pk=row[0]),segment=get_object_or_404(Segment, pk=row[1]),seat_free_date=row[2],free_seat=row[3])
        sf.save()
    f.close()

    print("DATABASE CREATED COMPLETE!")

    return render(request, 'turk/createdb.html')



