from django.contrib import admin

from .models import BillDetail, Guest, GuestBill, Payment, Reservation, Room, RoomType, Service, Staff


admin.site.register([Guest, Staff, RoomType, Room, Reservation, Service, GuestBill, BillDetail, Payment])
