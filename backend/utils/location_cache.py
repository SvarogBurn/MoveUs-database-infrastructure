"""
Redis-based location tracking
Handles real-time user location updates efficiently
"""
import redis
from django.conf import settings
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# Initialize Redis client
try:
    redis_client = redis.Redis(
        host=getattr(settings, 'REDIS_HOST', 'redis'),
        port=getattr(settings, 'REDIS_PORT', 6379),
        db=0,  # Use DB 0 for location data
        decode_responses=True,
        socket_timeout=5,
        socket_connect_timeout=5,
        retry_on_timeout=True,
    )
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None


def update_user_location(user_id: int, latitude: float, longitude: float, ttl: int = 300) -> bool:
    """
    Store user location in Redis with TTL
    
    Args:
        user_id: User ID
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        ttl: Time to live in seconds (default: 5 minutes)
    
    Returns:
        bool: True if successful, False otherwise
    
    Example:
        >>> update_user_location(123, 45.8, 15.9)
        True
    """
    if not redis_client:
        logger.error("Redis client not available")
        return False
    
    try:
        # Store in Redis geospatial index
        # GEOADD key longitude latitude member
        redis_client.geoadd(
            'user_locations',
            (longitude, latitude, f'user:{user_id}')
        )
        
        # Set expiration on the user's location
        redis_client.expire(f'user:{user_id}', ttl)
        
        logger.info(f"Updated location for user {user_id}: ({latitude}, {longitude})")
        return True
        
    except Exception as e:
        logger.error(f"Error updating location for user {user_id}: {e}")
        return False


def get_user_location(user_id: int) -> Optional[Tuple[float, float]]:
    """
    Get user's current location from Redis
    
    Args:
        user_id: User ID
    
    Returns:
        Tuple of (latitude, longitude) or None if not found
    
    Example:
        >>> get_user_location(123)
        (45.8, 15.9)
    """
    if not redis_client:
        return None
    
    try:
        position = redis_client.geopos('user_locations', f'user:{user_id}')
        
        if position and position[0]:
            lon, lat = position[0]
            return (float(lat), float(lon))
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting location for user {user_id}: {e}")
        return None


def get_nearby_users(
    latitude: float,
    longitude: float,
    radius_km: float = 5,
    unit: str = 'km',
    limit: int = 100
) -> List[Tuple[int, float]]:
    """
    Find users within radius of a location
    
    Args:
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers
        unit: Distance unit ('m', 'km', 'mi', 'ft')
        limit: Maximum number of users to return
    
    Returns:
        List of tuples (user_id, distance) sorted by distance
    
    Example:
        >>> get_nearby_users(45.8, 15.9, radius_km=5)
        [(123, 0.5), (456, 2.3), (789, 4.1)]
    """
    if not redis_client:
        return []
    
    try:
        # GEORADIUS key longitude latitude radius unit [WITHDIST] [COUNT count]
        results = redis_client.georadius(
            'user_locations',
            longitude,
            latitude,
            radius_km,
            unit=unit,
            withdist=True,
            count=limit,
            sort='ASC'  # Closest first
        )
        
        # Parse results: [('user:123', '0.5'), ('user:456', '2.3')]
        nearby_users = []
        for member, distance in results:
            if member.startswith('user:'):
                user_id = int(member.split(':')[1])
                nearby_users.append((user_id, float(distance)))
        
        return nearby_users
        
    except Exception as e:
        logger.error(f"Error finding nearby users: {e}")
        return []


def remove_user_location(user_id: int) -> bool:
    """
    Remove user location from Redis (e.g., on logout)
    
    Args:
        user_id: User ID
    
    Returns:
        bool: True if successful
    """
    if not redis_client:
        return False
    
    try:
        redis_client.zrem('user_locations', f'user:{user_id}')
        logger.info(f"Removed location for user {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error removing location for user {user_id}: {e}")
        return False


def get_active_users_count() -> int:
    """
    Get count of users with active location data
    
    Returns:
        int: Number of active users
    """
    if not redis_client:
        return 0
    
    try:
        return redis_client.zcard('user_locations')
    except Exception as e:
        logger.error(f"Error getting active users count: {e}")
        return 0


# Health check function
def redis_health_check() -> bool:
    """
    Check if Redis is accessible
    
    Returns:
        bool: True if Redis is healthy
    """
    if not redis_client:
        return False
    
    try:
        return redis_client.ping()
    except Exception:
        return False