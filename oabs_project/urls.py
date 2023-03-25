from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('users_app.urls')),
    path('appointment/', include('appointments_app.urls')),
    path('api/', include('apis.urls')),
    path('admin/', admin.site.urls),
]
