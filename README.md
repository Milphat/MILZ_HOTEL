# MILZ GRAND HOTEL — Django Hotel Management System

A Django application for hotel operations and customer room reservations.

The design follows a clear Booking.com-style separation of roles:

- **Guests** request rooms and track their bookings.
- **Administrators** manage inventory, confirm/cancel reservations and oversee hotel operations. They are controllers, not another kind of customer.

## Project Team Members

The following students contributed to the development of the MILZ Grand Hotel Management System:

| Registration Number | Full Name |
|---|---|
| 224-063061-28847 | NAJJINGO MILPHAT |
| 224-063061-29951 | KYAKWERA PHIONA |
| 224-063011-29949 | NAGGITA RAYAT |

## Features

- Customer registration, login and logout using Django authentication.
- Role-based redirects after sign-in and registration:
  - Staff and superusers go to the **Administrator Dashboard**.
  - Regular customers go to the hotel home page.
- Guests can request rooms using check-in/check-out dates and view their bookings.
- Administrator accounts are blocked from guest booking forms and My Bookings pages.
- Booking validation prevents overlapping pending or confirmed reservations for the same room.
- Staff can **Confirm** or **Cancel** reservations.
- Confirming a reservation updates the room's occupancy status.
- Cancelling can free a room when no other active booking holds it.
- Dashboard overview for rooms, reservations, guests, staff, services and unpaid bills.
- Full CRUD management for:
  - Guests
  - Staff
  - Room types
  - Rooms
  - Reservations
  - Services
  - Guest bills
  - Bill details
  - Payments
- Modern home page layout with prominent gold action buttons and role-specific calls to action.

## Requirements

- Python 3.10+
- Django 5.2 or newer (below 6.2)

## Setup (macOS / Windows / Linux)

Open a terminal in the folder containing `manage.py` and run:

```bash
python -m venv .venv
```

Activate the environment:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install dependencies and prepare the database:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Administrator Access

Create an administrator account using:

```bash
python manage.py createsuperuser
```

Sign in through the normal login page. Staff and superuser accounts are automatically redirected to the **Administrator Dashboard**.

All hotel management pages (rooms, room types, reservations, guests, staff, services, bills and payments) are restricted to staff/superuser accounts.

Administrators should use the Reservations page to confirm guest requests rather than the public Book a Room flow.

You can also promote another account from the Django shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.get(username="your-username")
user.is_staff = True
user.save()
```

## Customer Workflow (Booking.com Style)

1. Register an account or sign in using a non-staff account.
2. From the home page or navigation, select **Book a Room**.
3. Complete guest details, select an available room and enter the required dates.
4. Submit the request. It is saved with **Pending** status.
5. Hotel staff review the request and **Confirm** or **Cancel** it.
6. Open **My Bookings** at any time to view the reservation status.

## Important Deployment Notes

This package is configured for local development with SQLite and `DEBUG=True`.

Before public deployment:

- Set a strong secret key using an environment variable.
- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Configure HTTPS and appropriate security settings.
- Use a production database.
- Configure a production-grade static-file server.

## Project Information

**Project Name:** MILZ GRAND HOTEL  
**Project Type:** Django-Based Hotel Management and Room Reservation System  
**Framework:** Django  
**Database:** SQLite (local development)  
**Architecture:** Role-Based Hotel Management System  

**Developed by:** The MILZ GRAND HOTEL Project Team