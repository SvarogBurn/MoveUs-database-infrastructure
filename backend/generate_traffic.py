"""
Traffic Generator for MoveUs - Creates realistic activity for Prometheus/Grafana monitoring

This script generates:
1. HTTP requests (fast, slow, errors)
2. Database operations (reads/writes)
3. Redis location updates
4. Celery background tasks
5. User interactions

Run with: docker-compose exec web python generate_traffic.py
"""

import random
import time
import requests
from django.utils import timezone
from datetime import timedelta
from django.contrib.gis.geos import Point

# Django setup
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moveus.settings')
django.setup()

from users.models import User, PsychologicalProfile, UserActivityProficiency
from activities.models import Activity
from events.models import Event, EventParticipation, UserInteraction, EventRequirements
from locations.models import Location
from utils.location_cache import update_user_location
from core.enums import Gender, ActivityProficiency as ProficiencyEnum, InteractionType


class TrafficGenerator:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.activities = list(Activity.objects.all())
        self.users = list(User.objects.all())
        self.locations = list(Location.objects.all())
        
        if not self.users:
            print("⚠️  No users found! Run: docker-compose exec web python manage.py createsuperuser")
            exit(1)
    
    def generate_sample_data(self):
        """Create initial sample data if database is empty"""
        print("\n📊 Creating sample data...")
        
        # Create activities if none exist
        if not self.activities:
            activities_data = [
                {"name": "Basketball", "metabolic_demand": 0.8, "neurocognitive_precision": 0.7, 
                 "risk_modulation": 0.5, "kinesthetic_intelligence": 0.8, "environmental_dependency": 0.4, 
                 "collaborative_dynamics": 0.9},
                {"name": "Yoga", "metabolic_demand": 0.4, "neurocognitive_precision": 0.6, 
                 "risk_modulation": 0.1, "kinesthetic_intelligence": 0.7, "environmental_dependency": 0.2, 
                 "collaborative_dynamics": 0.3},
                {"name": "Running", "metabolic_demand": 0.9, "neurocognitive_precision": 0.3, 
                 "risk_modulation": 0.3, "kinesthetic_intelligence": 0.5, "environmental_dependency": 0.6, 
                 "collaborative_dynamics": 0.1},
                {"name": "Swimming", "metabolic_demand": 0.8, "neurocognitive_precision": 0.5, 
                 "risk_modulation": 0.4, "kinesthetic_intelligence": 0.7, "environmental_dependency": 0.8, 
                 "collaborative_dynamics": 0.3},
                {"name": "Rock Climbing", "metabolic_demand": 0.7, "neurocognitive_precision": 0.8, 
                 "risk_modulation": 0.9, "kinesthetic_intelligence": 0.9, "environmental_dependency": 0.7, 
                 "collaborative_dynamics": 0.5},
            ]
            for activity_data in activities_data:
                Activity.objects.create(**activity_data)
            self.activities = list(Activity.objects.all())
            print(f"✅ Created {len(self.activities)} activities")
        
        # Create locations if none exist
        if not self.locations:
            locations_data = [
                {"country": "Croatia", "city": "Zagreb", "postal_code": "10000", 
                 "point": Point(15.9819, 45.8150)},
                {"country": "Croatia", "city": "Split", "postal_code": "21000", 
                 "point": Point(16.4402, 43.5081)},
                {"country": "Croatia", "city": "Rijeka", "postal_code": "51000", 
                 "point": Point(14.4422, 45.3271)},
                {"country": "USA", "city": "New York", "postal_code": "10001", 
                 "point": Point(-74.0060, 40.7128)},
                {"country": "USA", "city": "San Francisco", "postal_code": "94102", 
                 "point": Point(-122.4194, 37.7749)},
            ]
            for loc_data in locations_data:
                Location.objects.create(**loc_data)
            self.locations = list(Location.objects.all())
            print(f"✅ Created {len(self.locations)} locations")
        
        # Create psychological profiles for users without them
        users_without_profiles = User.objects.filter(psychological_profile__isnull=True)
        for user in users_without_profiles:
            PsychologicalProfile.objects.create(
                user=user,
                openness=random.uniform(0.3, 0.9),
                conscientiousness=random.uniform(0.3, 0.9),
                extraversion=random.uniform(0.3, 0.9),
                agreeableness=random.uniform(0.3, 0.9),
                neuroticism=random.uniform(0.1, 0.7),
            )
        print(f"✅ Created psychological profiles")
        
        # Add activity proficiencies
        for user in self.users[:5]:  # Only first 5 users
            for activity in random.sample(self.activities, k=random.randint(2, 4)):
                UserActivityProficiency.objects.get_or_create(
                    user=user,
                    activity=activity,
                    defaults={"proficiency_level": random.choice([
                        ProficiencyEnum.BEGINNER,
                        ProficiencyEnum.INTERMEDIATE,
                        ProficiencyEnum.ADVANCED,
                    ])}
                )
        print(f"✅ Created activity proficiencies")
    
    def api_request_fast(self):
        """Fast API request - normal response time"""
        try:
            response = requests.get(f"{self.base_url}/api/health/", timeout=5)
            print(f"⚡ Fast request: {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Fast request failed: {e}")
            return False
    
    def api_request_slow(self):
        """Slow API request - simulates complex query"""
        try:
            # This will be slow if we add time.sleep in the view
            response = requests.get(f"{self.base_url}/api/events/nearby/", timeout=10)
            print(f"🐌 Slow request: {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
            return response.status_code
        except Exception as e:
            print(f"❌ Slow request failed: {e}")
            return False
    
    def api_request_error(self):
        """Request that causes an error"""
        try:
            # Request non-existent endpoint
            response = requests.get(f"{self.base_url}/api/nonexistent/endpoint/", timeout=5)
            print(f"💥 Error request: {response.status_code}")
            return response.status_code
        except Exception as e:
            print(f"❌ Error request failed: {e}")
            return False
    
    def create_event(self):
        """Create a new event - generates write traffic"""
        try:
            user = random.choice(self.users)
            activity = random.choice(self.activities)
            location = random.choice(self.locations)
            
            event = Event.objects.create(
                title=f"{activity.name} Session {random.randint(1, 1000)}",
                description=f"Join us for {activity.name}!",
                start_datetime=timezone.now() + timedelta(days=random.randint(1, 30)),
                end_datetime=timezone.now() + timedelta(days=random.randint(1, 30), hours=2),
                created_by=user,
                location=location,
                latitude=location.point.y if location.point else None,
                longitude=location.point.x if location.point else None,
                activity=activity,
            )
            
            # Add requirements
            EventRequirements.objects.create(
                event=event,
                min_age=random.choice([None, 18, 21]),
                max_age=random.choice([None, 40, 50, 60]),
                required_proficiency=random.choice([None, ProficiencyEnum.BEGINNER, ProficiencyEnum.INTERMEDIATE]),
            )
            
            print(f"📅 Created event: {event.title}")
            return event
        except Exception as e:
            print(f"❌ Failed to create event: {e}")
            return None
    
    def join_event(self):
        """User joins an event - generates participation"""
        try:
            user = random.choice(self.users)
            # Get future events
            future_events = Event.objects.filter(
                start_datetime__gte=timezone.now()
            ).exclude(
                participations__user=user
            )[:10]
            
            if not future_events:
                print("⚠️  No available events to join")
                return None
            
            event = random.choice(list(future_events))
            participation = EventParticipation.objects.create(
                user=user,
                event=event,
                rating=random.choice([None, 3, 4, 5]),  # Some have ratings
            )
            print(f"👥 {user.username} joined: {event.title}")
            return participation
        except Exception as e:
            print(f"❌ Failed to join event: {e}")
            return None
    
    def create_user_interaction(self):
        """Create user-to-user interaction"""
        try:
            if len(self.users) < 2:
                return None
            
            user1, user2 = random.sample(self.users, 2)
            
            # Get events both attended
            common_events = Event.objects.filter(
                participations__user=user1
            ).filter(
                participations__user=user2
            )
            
            if not common_events:
                print("⚠️  No common events for interaction")
                return None
            
            event = random.choice(list(common_events))
            
            interaction, created = UserInteraction.objects.get_or_create(
                from_user=user1,
                to_user=user2,
                event=event,
                defaults={
                    "interaction_value": random.choices(
                        [InteractionType.LIKE, InteractionType.NEUTRAL, InteractionType.DISLIKE],
                        weights=[0.6, 0.3, 0.1]  # More likes than dislikes
                    )[0]
                }
            )
            
            if created:
                print(f"🤝 {user1.username} → {user2.username}: {interaction.interaction_value}")
            return interaction
        except Exception as e:
            print(f"❌ Failed to create interaction: {e}")
            return None
    
    def update_redis_locations(self):
        """Update user locations in Redis"""
        try:
            user = random.choice(self.users)
            # Random location in Zagreb area
            lat = 45.8150 + random.uniform(-0.1, 0.1)
            lon = 15.9819 + random.uniform(-0.1, 0.1)
            
            success = update_user_location(user.id, lat, lon, ttl=300)
            if success:
                print(f"📍 Updated location for {user.username}: ({lat:.4f}, {lon:.4f})")
            return success
        except Exception as e:
            print(f"❌ Failed to update location: {e}")
            return False
    
    def database_read_heavy(self):
        """Perform read-heavy operations"""
        try:
            # Complex query that hits replicas
            from django.db.models import Count, Avg
            
            result = Event.objects.using('replica1').annotate(
                participant_count=Count('participations'),
                avg_rating=Avg('participations__rating')
            ).filter(
                participant_count__gt=0
            )[:10]
            
            print(f"📖 Read query executed: {len(list(result))} results from replica")
            time.sleep(0.5)  # Simulate slow query
            return True
        except Exception as e:
            print(f"❌ Read query failed: {e}")
            return False
    
    def run_continuous(self, duration_minutes=5):
        """Run continuous traffic generation"""
        print(f"\n🚀 Starting traffic generation for {duration_minutes} minutes...")
        print("=" * 60)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        # Generate sample data first
        self.generate_sample_data()
        
        iteration = 0
        while time.time() < end_time:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Mix of operations with different probabilities
            operations = [
                (self.api_request_fast, 0.4),        # 40% - Fast requests
                (self.api_request_slow, 0.1),        # 10% - Slow requests
                (self.api_request_error, 0.05),      # 5% - Errors
                (self.create_event, 0.08),           # 8% - Create events
                (self.join_event, 0.15),             # 15% - Join events
                (self.create_user_interaction, 0.07), # 7% - User interactions
                (self.update_redis_locations, 0.1),  # 10% - Location updates
                (self.database_read_heavy, 0.05),    # 5% - Heavy reads
            ]
            
            # Execute random operation
            operation, _ = random.choices(operations, weights=[w for _, w in operations])[0]
            operation()
            
            # Random sleep between operations
            sleep_time = random.uniform(0.5, 2.0)
            time.sleep(sleep_time)
        
        print("\n" + "=" * 60)
        print("✅ Traffic generation completed!")
        self.print_summary()
    
    def print_summary(self):
        """Print summary of database state"""
        from django.db.models import Count
        
        print("\n📊 DATABASE SUMMARY:")
        print(f"  Users: {User.objects.count()}")
        print(f"  Activities: {Activity.objects.count()}")
        print(f"  Events: {Event.objects.count()}")
        print(f"  Event Participations: {EventParticipation.objects.count()}")
        print(f"  User Interactions: {UserInteraction.objects.count()}")
        print(f"  Locations: {Location.objects.count()}")
        print(f"  Psychological Profiles: {PsychologicalProfile.objects.count()}")
        
        print("\n🔥 TOP METRICS TO CHECK IN PROMETHEUS:")
        print("  1. up{job='django'}")
        print("  2. rate(django_http_requests_total_by_view_transport_method_total[1m])")
        print("  3. django_http_requests_latency_seconds_by_view_method_bucket")
        print("  4. pg_stat_database_numbackends{datname='moveus_db'}")
        print("  5. redis_memory_used_bytes")
        print("  6. pg_stat_database_tup_fetched")
        print("  7. django_http_responses_total_by_status_total")
        
        print("\n📈 CHECK THESE IN GRAFANA:")
        print("  - Request rate (successful vs errors)")
        print("  - Response time percentiles (p50, p95, p99)")
        print("  - Database connections (primary vs replicas)")
        print("  - Redis memory growth")
        print("  - HTTP status code distribution")


def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         MoveUs Traffic Generator                         ║
    ║  Generates realistic activity for monitoring metrics     ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    generator = TrafficGenerator()
    
    # Run for 5 minutes (adjust as needed)
    generator.run_continuous(duration_minutes=5)


if __name__ == "__main__":
    main()