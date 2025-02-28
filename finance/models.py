from django.db import models
from accounts.models import User
from academics.models import ClassArm
from django.contrib.auth import get_user_model

class FeeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class FeeStructure(models.Model):
    class_arm = models.ForeignKey(ClassArm, on_delete=models.CASCADE)
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    session = models.CharField(max_length=10)  # E.g., 2024/2025
    term = models.CharField(max_length=20, choices=[("First Term", "First Term"), ("Second Term", "Second Term"), ("Third Term", "Third Term")])

    class Meta:
        unique_together = ('class_arm', 'fee_category', 'session', 'term')

    def __str__(self):
        return f"{self.class_arm} - {self.fee_category} - {self.amount}"

class Discount(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    fee_category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Discount percentage (e.g., 10 for 10%)")
    reason = models.TextField()

    def __str__(self):
        return f"{self.student.username} - {self.fee_category} ({self.percentage}%)"

class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, choices=[("Bank Transfer", "Bank Transfer"), ("Online", "Online"), ("Cash", "Cash")])
    reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.student.username} - {self.amount_paid} on {self.payment_date}"
    
class PaymentSummary:
    def __init__(self, student, session, term):
        self.student = student
        self.session = session
        self.term = term

    def total_fees_due(self):
        fees = FeeStructure.objects.filter(class_arm=self.student.class_arm, session=self.session, term=self.term)
        return sum(fee.amount for fee in fees)

    def total_discounts(self):
        discounts = Discount.objects.filter(student=self.student)
        return sum((discount.percentage / 100) * discount.fee_category.amount for discount in discounts)

    def total_paid(self):
        payments = Payment.objects.filter(student=self.student)
        return sum(payment.amount_paid for payment in payments)

    def balance_due(self):
        return self.total_fees_due() - self.total_discounts() - self.total_paid()

User = get_user_model()

class FeeStructure(models.Model):
    """ Defines different types of fees per class level """
    CLASS_LEVELS = [
        ('JSS1', 'Junior Secondary 1'),
        ('JSS2', 'Junior Secondary 2'),
        ('JSS3', 'Junior Secondary 3'),
        ('SS1', 'Senior Secondary 1'),
        ('SS2', 'Senior Secondary 2'),
        ('SS3', 'Senior Secondary 3'),
    ]

    class_level = models.CharField(max_length=10, choices=CLASS_LEVELS)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hostel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def total_fee(self):
        return self.tuition_fee + self.transport_fee + self.hostel_fee

    def __str__(self):
        return f"{self.class_level} Fee Structure"


class Discount(models.Model):
    """ Discounts offered to students (e.g., sibling discount, early payment) """
    name = models.CharField(max_length=100)
    percentage = models.FloatField()  # e.g., 10% discount
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.percentage}%"


class Scholarship(models.Model):
    """ Scholarships awarded to students """
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name="scholarship")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()

    def __str__(self):
        return f"{self.student.username} - Scholarship"


User = get_user_model()

class StudentPayment(models.Model):
    """ Stores each student's payment details """
class StudentPayment(models.Model):
    """ Stores each student's payment details """
    PAYMENT_METHODS = [
        ('paystack', 'Paystack'),
        ('flutterwave', 'Flutterwave'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    class_level = models.ForeignKey("FeeStructure", on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='paystack')
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.payment_status}"


    def total_due(self):
        """ Calculate total fee after applying discount/scholarship """
        total_fee = self.class_level.total_fee()

        if self.discount:
            total_fee -= (self.discount.percentage / 100) * total_fee

        if self.scholarship:
            total_fee -= self.scholarship.amount

        return max(total_fee - self.amount_paid, 0)

    def __str__(self):
        return f"{self.student.username} - {self.payment_status}"
