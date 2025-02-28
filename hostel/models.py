from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.TextField()
    total_rooms = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    available_beds = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class StudentRoomAllocation(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name="room_allocation")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="students")
    allocated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.room.room_number}"


User = get_user_model()

class HostelFeePayment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hostel_payments")
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20, 
        choices=[("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed")], 
        default="pending"
    )
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.hostel.name} - {self.payment_status}"
