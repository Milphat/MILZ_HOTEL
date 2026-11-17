from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings


class Guest(models.Model):
	class Gender(models.TextChoices):
		MALE = "Male", "Male"
		FEMALE = "Female", "Female"
		OTHER = "Other", "Other"

	guest_id = models.CharField(max_length=20, primary_key=True)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="hotel_guest")
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	contact = models.CharField(max_length=30)
	email = models.EmailField()
	address = models.CharField(max_length=200)
	nationality = models.CharField(max_length=80)
	gender = models.CharField(max_length=10, choices=Gender.choices)

	class Meta:
		ordering = ["guest_id"]

	def __str__(self):
		return f"{self.guest_id} - {self.first_name} {self.last_name}"


class Staff(models.Model):
	class Gender(models.TextChoices):
		MALE = "Male", "Male"
		FEMALE = "Female", "Female"
		OTHER = "Other", "Other"

	staff_id = models.CharField(max_length=20, primary_key=True)
	first_name = models.CharField(max_length=80)
	last_name = models.CharField(max_length=80)
	email = models.EmailField()
	contact = models.CharField(max_length=30)
	role = models.CharField(max_length=80)
	salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	gender = models.CharField(max_length=10, choices=Gender.choices)

	class Meta:
		ordering = ["staff_id"]

	def __str__(self):
		return f"{self.staff_id} - {self.first_name} {self.last_name}"


class RoomType(models.Model):
	room_type_id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=80)
	description = models.TextField()
	capacity = models.PositiveSmallIntegerField()
	price_per_night = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

	class Meta:
		ordering = ["room_type_id"]

	def __str__(self):
		return f"{self.room_type_id} - {self.name}"


class Room(models.Model):
	room_available = [
		('Single','single'),
		('Double','double'),
		('Suite','suite'),
		('Deluxe','deluxe')
	]
	class Status(models.TextChoices):
		AVAILABLE = "Available", "Available"
		OCCUPIED = "Occupied", "Occupied"
		MAINTENANCE = "Maintenance", "Maintenance"

	room_id = models.CharField(max_length=20, primary_key=True)
	room_type = models.CharField(max_length=20, choices=room_available)
	room_number = models.CharField(max_length=20, unique=True)
	floor = models.PositiveSmallIntegerField()
	status = models.CharField(max_length=20, choices=Status.choices)

	class Meta:
		ordering = ["room_id"]

	def __str__(self):
		return f"{self.room_id} - Room {self.room_number}"


class Reservation(models.Model):
	class Status(models.TextChoices):
		PENDING = "Pending", "Pending"
		CONFIRMED = "Confirmed", "Confirmed"
		CANCELLED = "Cancelled", "Cancelled"

	reservation_id = models.CharField(max_length=20, primary_key=True)
	guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name="reservations")
	room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="reservations")
	reservation_date = models.DateField()
	check_in_date = models.DateField()
	check_out_date = models.DateField()
	status = models.CharField(max_length=20, choices=Status.choices)

	class Meta:
		ordering = ["reservation_id"]

	def __str__(self):
		return self.reservation_id


class Service(models.Model):
	class Availability(models.TextChoices):
		AVAILABLE = "Available", "Available"
		UNAVAILABLE = "Unavailable", "Unavailable"

	service_id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=100)
	description = models.TextField()
	cost = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	availability = models.CharField(max_length=20, choices=Availability.choices)

	class Meta:
		ordering = ["service_id"]

	def __str__(self):
		return f"{self.service_id} - {self.name}"


class GuestBill(models.Model):
	class Status(models.TextChoices):
		PAID = "Paid", "Paid"
		NOT_PAID = "Not Paid", "Not Paid"

	bill_id = models.CharField(max_length=20, primary_key=True)
	guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name="bills")
	reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, related_name="bills")
	total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	tax = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	discount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	final_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	bill_date = models.DateField()
	status = models.CharField(max_length=20, choices=Status.choices)

	class Meta:
		ordering = ["bill_id"]

	def __str__(self):
		return self.bill_id


class BillDetail(models.Model):
	detail_id = models.CharField(max_length=20, primary_key=True)
	bill = models.ForeignKey(GuestBill, on_delete=models.CASCADE, related_name="details")
	service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="bill_details")
	quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
	unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	total_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

	class Meta:
		ordering = ["detail_id"]

	def __str__(self):
		return self.detail_id


class Payment(models.Model):
	class Method(models.TextChoices):
		CASH = "Cash", "Cash"
		MOBILE_MONEY = "Mobile Money", "Mobile Money"
		CREDIT_CARD = "Credit Card", "Credit Card"
		BANK_TRANSFER = "Bank Transfer", "Bank Transfer"

	class Status(models.TextChoices):
		PAID = "Paid", "Paid"
		PENDING = "Pending", "Pending"
		FAILED = "Failed", "Failed"
		

	payment_id = models.CharField(max_length=20, primary_key=True)
	reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, related_name="payments")
	payment_date = models.DateField()
	amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	payment_method = models.CharField(max_length=20, choices=Method.choices)
	payment_status = models.CharField(max_length=20, choices=Status.choices)

	class Meta:
		ordering = ["payment_id"]

	def __str__(self):
		return self.payment_id
