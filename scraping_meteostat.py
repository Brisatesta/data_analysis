import pandas as pd
from meteostat import Point, Daily
from datetime import datetime, timedelta
import time
import random


# Funzione per ottenere i dati meteo
def get_weather_data(city, latitude, longitude):
    data = []
    for year in range(2000, datetime.now().year + 1):
        for month, day in [(1, 15), (7, 15)]:
            start = datetime(year, month, day)
            end = start + timedelta(days=1)

            location = Point(latitude, longitude)
            weather_data = Daily(location, start, end)
            weather_data = weather_data.fetch()

            if not weather_data.empty:
                data.append({
                    'city': city,
                    'date': start.strftime('%Y-%m-%d'),
                    'max_temp': weather_data['tmax'].values[0] if 'tmax' in weather_data else None,
                    'min_temp': weather_data['tmin'].values[0] if 'tmin' in weather_data else None,
                })

            # Pausa casuale tra 2 e 3 secondi
            time.sleep(random.uniform(2, 3))

    return data


# Elenco esteso delle capitali europee con coordinate approssimative
cities = [
    {'city': 'Rome', 'latitude': 41.9028, 'longitude': 12.4964},
    {'city': 'Berlin', 'latitude': 52.5200, 'longitude': 13.4050},
    {'city': 'Paris', 'latitude': 48.8566, 'longitude': 2.3522},
    {'city': 'Madrid', 'latitude': 40.4168, 'longitude': -3.7038},
    {'city': 'London', 'latitude': 51.5074, 'longitude': -0.1278},
    {'city': 'Vienna', 'latitude': 48.2082, 'longitude': 16.3738},
    {'city': 'Athens', 'latitude': 37.9838, 'longitude': 23.7275},
    {'city': 'Brussels', 'latitude': 50.8503, 'longitude': 4.3517},
    {'city': 'Budapest', 'latitude': 47.4979, 'longitude': 19.0402},
    {'city': 'Copenhagen', 'latitude': 55.6761, 'longitude': 12.5683},
    {'city': 'Dublin', 'latitude': 53.3498, 'longitude': -6.2603},
    {'city': 'Helsinki', 'latitude': 60.1695, 'longitude': 24.9354},
    {'city': 'Lisbon', 'latitude': 38.7223, 'longitude': -9.1393},
    {'city': 'Amsterdam', 'latitude': 52.3676, 'longitude': 4.9041},
    {'city': 'Oslo', 'latitude': 59.9139, 'longitude': 10.7522},
    {'city': 'Prague', 'latitude': 50.0755, 'longitude': 14.4378},
    {'city': 'Stockholm', 'latitude': 59.3293, 'longitude': 18.0686},
    {'city': 'Warsaw', 'latitude': 52.2297, 'longitude': 21.0122},
    {'city': 'Zurich', 'latitude': 47.3769, 'longitude': 8.5417},
    {'city': 'Moscow', 'latitude': 55.7558, 'longitude': 37.6173},
    {'city': 'Istanbul', 'latitude': 41.0082, 'longitude': 28.9784},
    # Aggiungi altre capitali qui
]

# Raccolta dei dati per tutte le città
all_weather_data = []
start_time = time.time()

for city in cities:
    city_data = get_weather_data(city['city'], city['latitude'], city['longitude'])
    all_weather_data.extend(city_data)

# Convertire i dati in DataFrame
df = pd.DataFrame(all_weather_data)

# Salvare in CSV
df.to_csv('european_capitals_weather.csv', index=False)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Tempo totale impiegato per lo scraping: {elapsed_time:.2f} secondi")
