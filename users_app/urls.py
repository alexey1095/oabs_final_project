from django.urls import path

from . import views


urlpatterns = [
    
    # return login page
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
    path('home/', views.home_view, name='home_page'),
]