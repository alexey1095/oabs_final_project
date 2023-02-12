from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from isoweek import Week

from users_app.models import Doctor
from apis.serializers import DoctorSerializer
from apis.serializers import BookedAppointmentSerializer
from apis.serializers import NewAppointmentSerializer
from appointments_app.models import Appointment


@api_view(['GET'])
def doctor_list(request):
    ''' return doctor list'''

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def booked_appointments_list(request, doctor_id, year, week_number):
    ''' return a list of booked timeslots'''

    if request.method == 'GET':

        w = Week(year, week_number)
        week_start_date = w.monday()
        week_end_date = w.sunday()

        booked_appointments = Appointment.objects.filter(
            Q(appointment_date__range=[week_start_date, week_end_date]),
            Q(doctor=doctor_id),
            Q(appointment_status="Confirmed") | Q(
                appointment_status="Requested")).order_by('appointment_date')

        serializer = BookedAppointmentSerializer(
            booked_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def book_appointment(request):
    ''' book appointment'''
    if request.method == 'POST':        
        serializer = NewAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
