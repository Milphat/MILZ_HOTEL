from django import forms

from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import BillDetail, Guest, GuestBill, Payment, Reservation, Room, RoomType, Service, Staff


class HotelModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class GuestForm(HotelModelForm):
    class Meta:
        model = Guest
        fields = ["guest_id", "first_name", "last_name", "contact", "email", "address", "nationality", "gender"]
        labels = {"guest_id": "Guest ID", "first_name": "First name", "last_name": "Last name"}


class StaffForm(HotelModelForm):
    class Meta:
        model = Staff
        fields = ["staff_id", "first_name", "last_name", "email", "contact", "role", "salary", "gender"]
        labels = {"staff_id": "Staff ID", "first_name": "First name", "last_name": "Last name"}


class RoomTypeForm(HotelModelForm):
    class Meta:
        model = RoomType
        fields = ["room_type_id", "name", "description", "capacity", "price_per_night"]
        labels = {"room_type_id": "Room type ID", "name": "Room type name"}


class RoomForm(HotelModelForm):
    class Meta:
        model = Room
        fields = ["room_id", "room_type", "room_number", "floor", "status"]
        labels = {"room_id": "Room ID", "room_type": "Room type", "room_number": "Room number"}


class ReservationForm(HotelModelForm):
    class Meta:
        model = Reservation
        fields = ["reservation_id", "guest", "room", "reservation_date", "check_in_date", "check_out_date", "status"]
        labels = {"reservation_id": "Reservation ID", "guest": "Guest", "room": "Room"}
        widgets = {
            "reservation_date": forms.DateInput(attrs={"type": "date"}),
            "check_in_date": forms.DateInput(attrs={"type": "date"}),
            "check_out_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in_date")
        check_out = cleaned_data.get("check_out_date")
        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out_date", "Check-out must be after check-in.")
        return cleaned_data


class ServiceForm(HotelModelForm):
    class Meta:
        model = Service
        fields = ["service_id", "name", "description", "cost", "availability"]
        labels = {"service_id": "Service ID", "name": "Service name", "cost": "Service cost"}


class GuestBillForm(HotelModelForm):
    class Meta:
        model = GuestBill
        fields = ["bill_id", "guest", "reservation", "total_amount", "tax", "discount", "final_amount", "bill_date", "status"]
        labels = {"bill_id": "Bill ID", "guest": "Guest", "reservation": "Reservation"}
        widgets = {"bill_date": forms.DateInput(attrs={"type": "date"})}


class BillDetailForm(HotelModelForm):
    class Meta:
        model = BillDetail
        fields = ["detail_id", "bill", "service", "quantity", "unit_price", "total_amount"]
        labels = {"detail_id": "Bill detail ID", "bill": "Bill", "service": "Service"}


class PaymentForm(HotelModelForm):
    class Meta:
        model = Payment
        fields = ["payment_id", "reservation", "payment_date", "amount", "payment_method", "payment_status"]
        labels = {
            "payment_id": "Payment ID",
            "reservation": "Reservation",
            "payment_method": "Payment method",
            "payment_status": "Payment status",
        }
        widgets = {"payment_date": forms.DateInput(attrs={"type": "date"})}


class HotelLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username", "autocomplete": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password", "autocomplete": "current-password"}))

class CustomerBookingForm(forms.Form):
    first_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"class": "form-control"}))
    contact = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    nationality = forms.CharField(max_length=80, widget=forms.TextInput(attrs={"class": "form-control"}))
    gender = forms.ChoiceField(choices=Guest.Gender.choices, widget=forms.Select(attrs={"class": "form-control"}))
    room = forms.ModelChoiceField(queryset=Room.objects.none(), widget=forms.Select(attrs={"class": "form-control"}))
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["room"].queryset = Room.objects.filter(status=Room.Status.AVAILABLE)

    def clean(self):
        cleaned = super().clean()
        start, end, room = cleaned.get("check_in_date"), cleaned.get("check_out_date"), cleaned.get("room")
        if start and start < timezone.localdate():
            self.add_error("check_in_date", "Check-in cannot be in the past.")
        if start and end and end <= start:
            self.add_error("check_out_date", "Check-out must be after check-in.")
        if start and end and room:
            conflicts = Reservation.objects.filter(
                room=room,
                status__in=[Reservation.Status.PENDING, Reservation.Status.CONFIRMED],
                check_in_date__lt=end, check_out_date__gt=start,
            )
            if conflicts.exists():
                self.add_error("room", "This room is already booked for some or all of those dates. Please choose another room or dates.")
        return cleaned
