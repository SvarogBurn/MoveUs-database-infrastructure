"""
docker-compose run --rm -T web python manage.py shell < generate_big_data.py

"""

import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from activities.models import Activity
from locations.models import Location
from events.models import Event, EventParticipation
from users.models import PsychologicalProfile, UserActivityProficiency

User = get_user_model()

# Simple config
NUM_USERS = 10000
NUM_EVENTS = 5000
NUM_LOCATIONS = 20

print("Starting data generation...")

# 1. Create Activities
print("Creating activities...")
activities_data = [
    {'name': 'Running', 'metabolic_demand': 0.8, 'neurocognitive_precision': 0.3, 'risk_modulation': 0.4, 'kinesthetic_intelligence': 0.5, 'environmental_dependency': 0.6, 'collaborative_dynamics': 0.2},
    {'name': 'Cycling', 'metabolic_demand': 0.7, 'neurocognitive_precision': 0.4, 'risk_modulation': 0.5, 'kinesthetic_intelligence': 0.6, 'environmental_dependency': 0.7, 'collaborative_dynamics': 0.3},
    {'name': 'Swimming', 'metabolic_demand': 0.9, 'neurocognitive_precision': 0.5, 'risk_modulation': 0.3, 'kinesthetic_intelligence': 0.7, 'environmental_dependency': 0.8, 'collaborative_dynamics': 0.2},
    {'name': 'Yoga', 'metabolic_demand': 0.3, 'neurocognitive_precision': 0.6, 'risk_modulation': 0.1, 'kinesthetic_intelligence': 0.8, 'environmental_dependency': 0.2, 'collaborative_dynamics': 0.4},
    {'name': 'Football', 'metabolic_demand': 0.8, 'neurocognitive_precision': 0.7, 'risk_modulation': 0.6, 'kinesthetic_intelligence': 0.7, 'environmental_dependency': 0.5, 'collaborative_dynamics': 0.9},
]

activities = []
for data in activities_data:
    activity, _ = Activity.objects.get_or_create(name=data['name'], defaults=data)
    activities.append(activity)
print(f"✓ {len(activities)} activities")

# 2. Create Locations
print("Creating locations...")
locations = []
for i in range(NUM_LOCATIONS):
    lat = 45.8150 + random.uniform(-0.3, 0.3)
    lon = 15.9819 + random.uniform(-0.3, 0.3)
    loc = Location.objects.create(
        country='Croatia',
        city='Zagreb',
        postal_code=f"100{i:02d}",
        point=Point(lon, lat, srid=4326)
    )
    locations.append(loc)
print(f"✓ {len(locations)} locations")

# 3. Create Users
print("Creating users...")
users = []
for i in range(NUM_USERS):
    user = User.objects.create_user(
        username=f"user{i:04d}",
        email=f"user{i:04d}@test.com",
        password='test123',
        first_name=f"User{i}",
        last_name="Test",
        gender=random.choice(['M', 'F', 'O']),
        home_city=random.choice(locations),
        indoor_outdoor_preference=random.choice(['IND', 'OUT', 'NO']),
        frequency_of_physical_activity=random.randint(0, 20),
        desired_frequency_of_physical_activity=random.randint(0, 30),
    )
    
    # Create psychological profile
    PsychologicalProfile.objects.create(
        user=user,
        openness=random.uniform(0, 1),
        conscientiousness=random.uniform(0, 1),
        extraversion=random.uniform(0, 1),
        agreeableness=random.uniform(0, 1),
        neuroticism=random.uniform(0, 1),
    )
    
    # Add 1-3 activity proficiencies
    for activity in random.sample(activities, random.randint(1, 3)):
        UserActivityProficiency.objects.create(
            user=user,
            activity=activity,
            proficiency_level=random.choice(['BEG', 'INT', 'ADV'])
        )
    
    users.append(user)
    if (i + 1) % 10 == 0:
        print(f"  {i + 1}/{NUM_USERS} users...")

print(f"✓ {len(users)} users with profiles")

# 4. Create Events
print("Creating events...")
events = []
now = timezone.now()
for i in range(NUM_EVENTS):
    creator = random.choice(users)
    activity = random.choice(activities)
    location = random.choice(locations)
    
    start = now + timedelta(days=random.randint(-30, 60), hours=random.randint(6, 20))
    end = start + timedelta(hours=random.randint(1, 3))
    
    event = Event.objects.create(
        title=f"{activity.name} Session {i}",
        description=f"Join us for {activity.name}!",
        start_datetime=start,
        end_datetime=end,
        location=location,
        location_point=location.point,
        address=f"Address {i}",
        created_by=creator,
        activity=activity,
    )
    events.append(event)
    
    # Creator participates
    EventParticipation.objects.create(user=creator, event=event)
    
    # Add 0-3 more participants
    for participant in random.sample(users, random.randint(0, 3)):
        if participant != creator:
            EventParticipation.objects.create(user=participant, event=event)
    
    if (i + 1) % 10 == 0:
        print(f"  {i + 1}/{NUM_EVENTS} events...")

print(f"✓ {len(events)} events")

# Summary
print("\n" + "="*50)
print("DATA GENERATION COMPLETE!")
print("="*50)
print(f"Activities:      {Activity.objects.count()}")
print(f"Locations:       {Location.objects.count()}")
print(f"Users:           {User.objects.count()}")
print(f"Profiles:        {PsychologicalProfile.objects.count()}")
print(f"Proficiencies:   {UserActivityProficiency.objects.count()}")
print(f"Events:          {Event.objects.count()}")
print(f"Participations:  {EventParticipation.objects.count()}")
print("="*50)