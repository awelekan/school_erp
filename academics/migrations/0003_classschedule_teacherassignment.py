# Generated by Django 5.1.6 on 2025-02-26 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_subject'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('class_arm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='academics.classarm')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.subject')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('class_arm', 'subject', 'day_of_week', 'start_time')},
            },
        ),
        migrations.CreateModel(
            name='TeacherAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_arm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.classarm')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.subject')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('teacher', 'subject', 'class_arm')},
            },
        ),
    ]
