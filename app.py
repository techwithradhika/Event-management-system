from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import requests

app = FastAPI()

class Event(BaseModel):
    event_name: str
    city_name: str
    date: str
    time: str
    latitude: float
    longitude: float

class EventResponse(BaseModel):
    message: str

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="",  # Replace with your MySQL password
        database="events_database"
    )

def insert_event(event: Event):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO events (event_name, city_name, date, time, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (event.event_name, event.city_name, event.date, event.time, event.latitude, event.longitude))
    connection.commit()
    connection.close()

@app.post('/api/events', response_model=EventResponse)
async def add_event(event: Event):
    insert_event(event)
    return {'message': 'Event added successfully'}

@app.get('/api/events/find')
async def find_events(latitude: float, longitude: float, date: str, page: int = 1, pageSize: int = 10):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM events
        WHERE date BETWEEN %s AND DATE_ADD(%s, INTERVAL 14 DAY)
    ''', (date, date))
    rows = cursor.fetchall()
    events = []
    for row in rows:
        event = {
            'event_name': row[1],  
            'city_name': row[2],   
            'date': row[3],        
            'time': row[4],        
            'latitude': row[5],    
            'longitude': row[6]   
        }
        weather = get_weather(event['city_name'], event['date'])
        distance = get_distance(latitude, longitude, event['latitude'], event['longitude'])
        event['weather'] = weather
        event['distance'] = distance
        events.append(event)
    connection.close()
    events.sort(key=lambda x: x['date'])
    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_events = events[start_index:end_index]
    total_events = len(events)
    total_pages = (total_events + pageSize - 1) // pageSize
    return {
        'events': paginated_events,
        'page': page,
        'pageSize': pageSize,
        'totalEvents': total_events,
        'totalPages': total_pages
    }

def get_weather(city_name: str, date: str):
    weather_api_url = f"https://gg-backend-assignment.azurewebsites.net/api/Weather?code=KfQnTWHJbg1giyB_Q9Ih3Xu3L9QOBDTuU5zwqVikZepCAzFut3rqsg==&city={city_name}&date={date}"
    response = requests.get(weather_api_url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather']
        return weather
    else:
        return "Weather data not available"

def get_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    distance_api_url = f"https://gg-backend-assignment.azurewebsites.net/api/Distance?code=IAKvV2EvJa6Z6dEIUqqd7yGAu7IZ8gaH-a0QO6btjRc1AzFu8Y3IcQ==&latitude1={lat1}&longitude1={lon1}&latitude2={lat2}&longitude2={lon2}"
    response = requests.get(distance_api_url)
    if response.status_code == 200:
        data = response.json()
        distance_km = data['distance']
        return distance_km
    else:
        return "Distance data not available"
