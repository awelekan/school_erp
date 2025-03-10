# Generated by Django 5.1.6 on 2025-02-26 19:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transportfee',
            name='due_date',
        ),
        migrations.RemoveField(
            model_name='transportfee',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='transportfee',
            name='payment',
        ),
        migrations.AddField(
            model_name='transportfee',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transportfee',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transportfee',
            name='payment_method',
            field=models.CharField(choices=[('paystack', 'Paystack'), ('flutterwave', 'Flutterwave'), ('bank_transfer', 'Bank Transfer'), ('cash', 'Cash')], default='paystack', max_length=20),
        ),
        migrations.AddField(
            model_name='transportfee',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed')], default='pending', max_length=10),
        ),
        migrations.AddField(
            model_name='transportfee',
            name='transaction_ref',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='transportfee',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_fees', to=settings.AUTH_USER_MODEL),
        ),
    ]
