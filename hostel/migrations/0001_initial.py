# Generated by Django 5.1.6 on 2025-02-26 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.TextField()),
                ('total_rooms', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=10, unique=True)),
                ('capacity', models.PositiveIntegerField()),
                ('available_beds', models.PositiveIntegerField()),
                ('hostel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hostel.hostel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentRoomAllocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allocated_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='hostel.room')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='room_allocation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
