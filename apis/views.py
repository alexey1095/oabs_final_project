from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Q
from isoweek import Week
from users_app.models import Doctor
from apis.serializers import DoctorSerializer
from apis.serializers import BookedAppointmentSerializer
from apis.serializers import NewAppointmentSerializer
from apis.serializers import RequestDaysOffSerializer
from apis.serializers import ConfirmAppointmentSerializer
from apis.serializers import RegisterNewPatientSerializer
from apis.serializers import AddToWishListSerializer
from appointments_app.models import Appointment

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def doctor_list(request):
    ''' return doctor list'''

    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
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
@permission_classes((IsAuthenticated, ))
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


@api_view(['PATCH'])
@permission_classes((IsAuthenticated, ))
def confirm_appointment(request, appointment_id):
    ''' confirm appointment'''
    if request.method == 'PATCH':

        try:
            appointment = Appointment.objects.get(pk=appointment_id)

        except Appointment.DoesNotExist:
            return Response("Appointment does not exist",
                        status=status.HTTP_400_BAD_REQUEST)
        

        if appointment.doctor.user != request.user:
            return Response("Wrong doctor. The appointment confirmation can only be made by the doctor who owns the appointment. ",
                        status=status.HTTP_400_BAD_REQUEST)


        serializer = ConfirmAppointmentSerializer(appointment, data={'appointment_status':'Confirmed'}, partial=True)
        if serializer.is_valid():

            serializer.save()
            
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_patient(request):
    ''' register patient '''
    if request.method == 'POST':        
        serializer = RegisterNewPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def request_daysoff(request):
    ''' request days off '''
    if request.method == 'POST':        
        serializer = RequestDaysOffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_to_wishlist(request):
    ''' add to wish list '''
    if request.method == 'POST':        
        serializer = AddToWishListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

