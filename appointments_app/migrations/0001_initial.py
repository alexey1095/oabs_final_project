# Generated by Django 4.1.5 on 2023-02-25 19:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DaysOffStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DaysOff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_till', models.DateField()),
                ('comment', models.CharField(blank=True, max_length=256)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('daysoff_status', models.ForeignKey(default='Booked', on_delete=django.db.models.deletion.CASCADE, to='appointments_app.daysoffstatus', to_field='status')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateTimeField()),
                ('symptoms', models.CharField(max_length=256)),
                ('request_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('appointment_status', models.ForeignKey(default='Requested', on_delete=django.db.models.deletion.CASCADE, to='appointments_app.appointmentstatus', to_field='status')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_app.patient')),
            ],
        ),
        migrations.AddConstraint(
            model_name='daysoff',
            constraint=models.UniqueConstraint(fields=('doctor', 'date_from', 'date_till'), name='unique_daysoff_record'),
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.UniqueConstraint(condition=models.Q(('appointment_status', 'Requested'), ('appointment_status', 'Confirmed'), _connector='OR'), fields=('doctor', 'appointment_date', 'appointment_status'), name='unique_appointment'),
        ),
    ]
