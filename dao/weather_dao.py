from psycopg.rows import dict_row
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class WeatherRecord:
    weather_id: int
    city_id: int
    weather_date: date
    temp_mean_f: float
    temp_max_f: float
    temp_min_f: float
    precipitation_sum_in: float
    precipitation_hours: float
    wind_speed_max_mph: float

@dataclass
class MaxWeatherResponse:
     city_name: str
     temp_max_f: float

## =============================================================================
# DAO CLASS
# -`bulk_create(city_id, weather_date, temp_mean_f,temp_max_f,temp_min_f,precipitation_sum_in,precipitation_hours,wind_speed_max_mph)— insert records into weather table in bulk
# -`get_by_id(weather_id)` — return a single weather record by its ID

# =============================================================================

class WeatherDAO:
    def __init__(self,conn):
            # Connection string is built once at instantiation from environment
            # variables loaded by db_util in main. All methods reuse this value.
            self._conn = conn

    def _map_row(self, row) -> WeatherRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return WeatherRecord(
                weather_id=row["weather_id"],
                city_id=row["city_id"],
                weather_date=row["weather_date"],
                temp_mean_f=row["temp_mean_f"],
                temp_max_f=row["temp_max_f"],
                temp_min_f=row["temp_min_f"],
                precipitation_sum_in=row["precipitation_sum_in"],
                precipitation_hours=row["precipitation_hours"],
                wind_speed_max_mph=row["wind_speed_max_mph"]
            )
    

    def create(self,weather_df):
        data_to_insert = list(weather_df.itertuples(index=False, name=None))
        with self._conn.transaction():
              with self._conn.cursor() as cur:
                    cur.execute(
                          "TRUNCATE TABLE weather_analytics.weather CASCADE"
                    )
                    cur.executemany(
                        "INSERT INTO weather_analytics.weather (city_id,weather_date,temp_mean_f,temp_max_f,temp_min_f,precipitation_sum_in,precipitation_hours,wind_speed_max_mph) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        data_to_insert)
                    return cur.rowcount

    def  highest_temp_per_city(self):
        with self._conn.transaction():
            with self._conn.cursor() as cur:
                
                cur.execute(
                    """SELECT c.city,
                    MAX(w.temp_max_f)
                            FROM weather_analytics.weather w
          	            INNER JOIN weather_analytics.city c
                         	ON c.city_id = w.city_id
          	            GROUP BY c.city"""
                        
                )
                rows = cur.fetchall()
                
                #response = []

                if not rows:
                    print("No records found.")
                    return None
                else:
                    
                    return rows
    
    def lowest_temp_per_city(self):
          pass
    
    def total_monthly_precipitation_per_city(self):
          pass
    
    def total_hours_precipitation_per_city(self):
          pass
    
    def windiest_week_per_city(self):
          pass
    