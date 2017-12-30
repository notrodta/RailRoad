from django.contrib import admin
from .models import Train,Station,Stop,Passenger,Reservation,Segment,Seats_Free,Trip

admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Stop)
admin.site.register(Passenger)
admin.site.register(Reservation)
admin.site.register(Segment)
admin.site.register(Seats_Free)
admin.site.register(Trip)



