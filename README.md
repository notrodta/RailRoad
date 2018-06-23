# RailRoad - Database Project

This is a website that helps user buy tickets for the RailRoad.

To run project, please go into the following directory in your terminal: RailRoad/RST
Then run the command ```python manage.py runserver```

To go to the homepage, enter this url: http://127.0.0.1:8000/turk/front_page/

# Front Page:
The front page is the main page of the website. It allows you pick between weekend trains or weekday trains. It allows you to choose your station of origin and you destination station along with the date of your choice. It will then display all the available trains with their arrival time. Clicking on one of the available trains will bring you to the reservation page.

![alt tag](https://i.imgur.com/78Bw4bV.png)

# Reservation Page:
The reservation page is where the user will enter their information such as their first name, last name, and their billing address. When completed, the database will create a passenger record in the passenger table along with a reservation record and a trip record. Then the page will redirect you to reservation completion page, where it will show you your ticket informations.

![alt tag](https://i.imgur.com/L89SnpH.png)

# Confirm Reservation:
The confirm reservation page shows your ticket info. The ticket info shows your passenger ID, reservation ID, the train arrival time, the station of origin, the destination station, the fare and the date of the trip.

The two most important information here are the unique Passenger ID and the unique Reservation ID. When a user wants to cancel a reservation or rebook a trip, they will be required to fill in both their passenger and reservation ID to the system

![alt tag](https://i.imgur.com/cheJK8X.png)

# Cancelling/Rebook:
This page is where the user will need to go if they wish to cancel their reservation or rebook their trip. They are required to fill in their unique Passenger ID and their unique Reservation ID along with choosing an option between canceling or rebooking their trip.

![alt tag](https://i.imgur.com/KxZhkxP.png)

# Cancellation Confirmation:

This page is here to just inform the user that their reservation has been successfully canceled if they chose to cancel their reservation.

![alt tag](https://i.imgur.com/mAcRkBO.png)

For those who wish to rebook their trip, they will be redirect back to the main page where they will need to repick an available train again.
