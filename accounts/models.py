from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Superadmin'),
        ('controller', 'Controller'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('staff', 'Staff'),
        ('accountant', 'Accountant'),
    ]
    
    username = models.CharField(max_length=50, unique=True)  # Student/Teacher/Staff ID
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    email = models.EmailField(unique=False, blank=True, null=True)  # Not required for uniqueness
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'  # Use student/teacher/staff ID as login
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    def is_superadmin(self):
        return self.role == 'superadmin'

    def is_controller(self):
        return self.role == 'controller'

    def is_accountant(self):
        return self.role == 'accountant'

    def __str__(self):
        return f"{self.username} - {self.role}"
