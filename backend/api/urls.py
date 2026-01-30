from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health'),
    path('events/nearby/', views.NearbyEventsView.as_view(), name='nearby-events'),
    path('users/me/location/', views.UpdateLocationView.as_view(), name='update-location'),
    
]