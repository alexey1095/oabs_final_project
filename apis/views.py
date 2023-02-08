from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from users_app.models import Doctor
from apis.serializers import DoctorSerializer,  BookedAppointmentSerializer, NewAppointmentSerializer
from appointments_app.models import Appointment

#from django.contrib.auth.models import User
from django.db.models import Q
from isoweek import Week

# from rest_framework.parsers import JSONParser
# from django.http import JsonResponse


@api_view(['GET'])
def doctor_list(request):

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def booked_appointments_list(request, doctor_id, year, week_number):

    # should be like this path('calendar/<int:doctor_id>/<int:year>/<int:week_number>/',

    if request.method == 'GET':

        # year = 2023
        # week_number = 3
        # doctor_id = 1

        w = Week(year, week_number)
        week_start_date = w.monday()
        week_end_date = w.sunday()

        booked_appointments = Appointment.objects.filter(
            Q(appointment_date__range=[week_start_date, week_end_date]),
            Q(doctor=doctor_id),
            Q(appointment_status="Confirmed") | Q(
                appointment_status="Requested")).order_by('appointment_date')

        # appointments = .objects.all()
        serializer = BookedAppointmentSerializer(booked_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def book_appointment(request):
    if request.method == 'POST':
        # data = JSONParser().parse(request.data)
        serializer =  NewAppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)