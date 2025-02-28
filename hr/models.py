from django.db import models
from accounts.models import User

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role__in': ['teacher', 'staff', 'accountant']})
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"

class Payroll(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.CharField(max_length=20, choices=[
        ("January", "January"), ("February", "February"), ("March", "March"),
        ("April", "April"), ("May", "May"), ("June", "June"),
        ("July", "July"), ("August", "August"), ("September", "September"),
        ("October", "October"), ("November", "November"), ("December", "December")
    ])
    year = models.PositiveIntegerField()
    salary_paid = models.DecimalField(max_digits=10, decimal_places=2)
    tax_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[("Paid", "Paid"), ("Pending", "Pending")], default="Pending")
    pension_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Paid", "Paid")], default="Pending")

    def calculate_deductions(self):
        tax_rate = 0.07  # 7% Tax
        pension_rate = 0.075  # 7.5% Pension

        self.tax_deduction = self.salary_paid * tax_rate
        self.pension_deduction = self.salary_paid * pension_rate
        self.net_salary = self.salary_paid - self.tax_deduction - self.pension_deduction
        self.save()
    
    
    class Meta:
        unique_together = ('staff', 'month', 'year')

    def net_salary(self):
        return self.salary_paid + self.bonus - self.deductions

    def __str__(self):
        return f"{self.staff.user.username} - {self.month} {self.year} - {self.payment_status}"

class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("Present", "Present"), ("Absent", "Absent"), ("Leave", "Leave")])

    def __str__(self):
        return f"{self.staff.user.username} - {self.date} - {self.status}"

class Leave(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50, choices=[("Sick Leave", "Sick Leave"), ("Casual Leave", "Casual Leave"), ("Maternity Leave", "Maternity Leave")])
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[("Approved", "Approved"), ("Pending", "Pending"), ("Rejected", "Rejected")], default="Pending")

    def __str__(self):
        return f"{self.staff.user.username} - {self.leave_type} ({self.start_date} to {self.end_date})"

class Payroll(models.Model):
    APPROVAL_STATUS = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, default="Pending")

    def approve(self):
        self.approval_status = "Approved"
        self.payment_status = "Paid"
        self.save()
        
        
# class Payroll(models.Model):
#     staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     month = models.CharField(max_length=20)
#     year = models.IntegerField()
#     salary_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     tax_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    