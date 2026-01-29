from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.utils import timezone
from django.core.cache import cache
from utils.location_cache import update_user_location, get_nearby_users, redis_health_check


class NearbyEventsView(APIView):
    """
    GET /api/events/nearby/?lat=45.8&lon=15.9&radius=5
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        from events.models import Event
        
        try:
            lat = float(request.query_params.get('lat'))
            lon = float(request.query_params.get('lon'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid coordinates'}, status=status.HTTP_400_BAD_REQUEST)
        
        radius = float(request.query_params.get('radius', 5))
        user_location = Point(lon, lat, srid=4326)
        
        events = Event.objects.filter(
            location_point__distance_lte=(user_location, D(km=radius)),
            start_datetime__gte=timezone.now()
        ).select_related('activity', 'created_by')[:50]
        
        data = [{
            'id': e.id,
            'title': e.title,
            'start_datetime': e.start_datetime,
            'location': {'latitude': e.location_point.y, 'longitude': e.location_point.x},
            'activity': {'id': e.activity.id, 'name': e.activity.name} if e.activity else None,
        } for e in events]
        
        return Response(data)


class UpdateLocationView(APIView):
    """
    POST /api/users/me/location/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            lat = float(request.data.get('latitude'))
            lon = float(request.data.get('longitude'))
        except (TypeError, ValueError):
            return Response({'error': 'Invalid coordinates'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return Response({'error': 'Coordinates out of range'}, status=status.HTTP_400_BAD_REQUEST)
        
        success = update_user_location(request.user.id, lat, lon)
        
        if success:
            return Response({'message': 'Location updated'})
        else:
            return Response({'error': 'Failed to update location'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HealthCheckView(APIView):
    """
    GET /api/health/
    """
    permission_classes = []
    
    def get(self, request):
        from django.db import connection
        
        checks = {'database': False, 'redis': False, 'status': 'unhealthy'}
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            checks['database'] = True
        except Exception:
            pass
        
        checks['redis'] = redis_health_check()
        
        if checks['database'] and checks['redis']:
            checks['status'] = 'healthy'
            return Response(checks, status=status.HTTP_200_OK)
        else:
            return Response(checks, status=status.HTTP_503_SERVICE_UNAVAILABLE)