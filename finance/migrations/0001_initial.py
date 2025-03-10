# Generated by Django 5.1.6 on 2025-02-26 14:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academics', '0005_reportcard'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=2, help_text='Discount percentage (e.g., 10 for 10%)', max_digits=5)),
                ('reason', models.TextField()),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fee_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.feecategory')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(choices=[('Bank Transfer', 'Bank Transfer'), ('Online', 'Online'), ('Cash', 'Cash')], max_length=50)),
                ('reference', models.CharField(max_length=100, unique=True)),
                ('student', models.ForeignKey(limit_choices_to={'role': 'student'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FeeStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('session', models.CharField(max_length=10)),
                ('term', models.CharField(choices=[('First Term', 'First Term'), ('Second Term', 'Second Term'), ('Third Term', 'Third Term')], max_length=20)),
                ('class_arm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.classarm')),
                ('fee_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.feecategory')),
            ],
            options={
                'unique_together': {('class_arm', 'fee_category', 'session', 'term')},
            },
        ),
    ]
