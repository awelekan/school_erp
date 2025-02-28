from django.db import models
from accounts.models import User  # Assuming drivers are part of staff
from finance.models import Payment  # For fee tracking
from django.utils import timezone

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    assigned_driver = models.OneToOneField('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')

    def __str__(self):
        return f"Bus {self.bus_number} - {self.capacity} Seats"

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})  # Assuming drivers are part of staff
    license_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Route(models.Model):
    name = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    stops = models.ManyToManyField('Stop', related_name='routes')

    def __str__(self):
        return self.name

class Stop(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TransportFee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transport_fees")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=[
        ('paystack', 'Paystack'),
        ('flutterwave', 'Flutterwave'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ], default='paystack')
    transaction_ref = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    due_date = models.DateTimeField(default=timezone.now)  # Use timezone.now as the default value

    def __str__(self):
        return f"{self.student.username} - {self.amount} ({self.status})"

class StudentTransport(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    assigned_route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True)
    assigned_bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)
    transport_fee = models.ForeignKey(TransportFee, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.assigned_route}"

