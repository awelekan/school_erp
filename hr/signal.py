from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Payroll

@receiver(pre_save, sender=Payroll)
def auto_calculate_deductions(sender, instance, **kwargs):
    instance.calculate_deductions()
