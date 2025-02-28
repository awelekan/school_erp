from celery import shared_task
from django.core.mail import send_mail
from .models import StudentPayment
from django.utils import timezone
import datetime

@shared_task
def send_fee_reminders():
    today = timezone.now().date()
    unpaid_fees = StudentPayment.objects.filter(payment_status="pending")

    for payment in unpaid_fees:
        due_date = payment.class_level.fee_due_date  # Assuming there's a due date
        days_left = (due_date - today).days

        if days_left <= 5:  # Send reminders for fees due in 5 days or overdue
            send_mail(
                subject="School Fee Payment Reminder",
                message=f"Dear {payment.student.username},\n\nYour school fees of ₦{payment.class_level.fee_amount} is due on {due_date}. Please make payment before the due date to avoid penalties.",
                from_email="school@domain.com",
                recipient_list=[payment.student.email],
            )

    return "Reminders Sent!"
