# MILZ GRAND HOTEL — Django Hotel Management System

A Django application for hotel operations and customer room reservations.
The design follows a clear Booking.com-style separation of roles:

- **Guests** request rooms and track their bookings.
- **Administrators** own inventory, confirm/cancel requests and run operations.
  They are controllers, not another kind of customer.

## Features

- Customer registration, login and logout using Django authentication.
- Role-based redirect after sign-in / registration:
  - Staff and superusers go to the **Administrator dashboard**.
  - Regular customers go to the hotel home page.
- Guests can request a room for check-in/check-out dates and view their own bookings.
- Admin accounts are blocked from the guest booking form and “My bookings” pages.
- Booking validation prevents overlapping pending or confirmed reservations for the same room.
- Staff can **Confirm** or **Cancel** reservations from the Reservations page.
  Confirming marks the room Occupied; cancelling can free it when no other active booking holds it.
- Dashboard overview for rooms, reservations, guests, staff, services and unpaid bills.
- Full CRUD management pages for guests, staff, room types, rooms, reservations, services, guest bills, bill details and payments.
- Modern home page layout with highly visible gold action buttons and role-specific calls to action.

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

Open http://127.0.0.1:8000/ in your browser.

## Administrator access

Create an administrator account using `python manage.py createsuperuser`.
Sign in through the normal login page. Staff and superuser accounts are
automatically redirected to the **Administrator dashboard**.

All hotel management pages (rooms, room types, reservations, guests, staff,
services, bills, payments) are restricted to staff/superuser accounts.
Administrators should use the Reservations page to confirm guest requests —
they should not use the public “Book a room” flow.

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

## Customer workflow (Booking.com style)

1. Register an account or sign in (non-staff account).
2. From the home page or navigation choose **Book a room**.
3. Complete guest details, select an **Available** room and enter dates.
4. Submit the request. It is saved with **Pending** status.
5. Hotel staff review the request and **Confirm** or **Cancel** it.
6. Open **My bookings** at any time to see the current status.

## Important deployment notes

This package is configured for local development with SQLite and `DEBUG=True`.
Before public deployment, set a strong secret key through an environment variable,
set `DEBUG=False`, configure `ALLOWED_HOSTS`, HTTPS/security settings, and a
production database. Configure a production-grade static-file server as well.
# MILZ_HOTEL
