from django.core.management.base import BaseCommand
from django.utils.timezone import now
from hr.models import Staff, Payroll
from django.core.mail import send_mail

class Command(BaseCommand):
    help = "Automatically process payroll at the end of each month"

    def handle(self, *args, **kwargs):
        today = now().date()
        month = today.strftime("%B")
        year = today.year

        staff_list = Staff.objects.all()
        for staff in staff_list:
            if not Payroll.objects.filter(staff=staff, month=month, year=year).exists():
                Payroll.objects.create(
                    staff=staff,
                    month=month,
                    year=year,
                    salary_paid=staff.salary,
                    deductions=0,
                    bonus=0,
                    payment_status="Pending"
                )
                self.send_reminder(staff)

        self.stdout.write(self.style.SUCCESS(f"Payroll processed for {month} {year}."))

    def send_reminder(self, staff):
        send_mail(
            subject="Payroll Processed",
            message=f"Dear {staff.user.first_name}, your payroll for {now().date().strftime('%B %Y')} has been processed. Kindly check for approval.",
            from_email="admin@school.com",
            recipient_list=[staff.user.email]
        )
