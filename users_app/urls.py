from django.urls import path

from . import views


#app_name = 'appointments_app'
app_name = 'users_app'

urlpatterns = [
    
    # return login page
    path('', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
    path('registration/', views.registration_view, name='registration_page'),
    path('home/', views.home_view, name='home_page'),

]

