from django.urls import path
from apis import views

urlpatterns = [
    path('doctors/',
         views.doctor_list,
         name='doctor_list'),

    path('booked_appointments/<int:doctor_id>/<int:year>/<int:week_number>/',
         views.booked_appointments_list,
         name='booked_appointments_list'),
    # path('transformers/<int:pk>/',
    #      views.transformer_detail,
    #      name = 'employee-detail'),
]
