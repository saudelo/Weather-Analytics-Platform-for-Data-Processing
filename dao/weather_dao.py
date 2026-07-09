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
class WeatherResponse:
    city_name: str
    weather: float

@dataclass
class PrecipResponse:
    weather_date: date
    city_name: str
    precip: float

@dataclass
class WindResponse:
    city_name: str
    windiest_week: date
    wind_speed: float


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
                

                if not rows:
                    print("No records found.")
                    return None
                else:
                    response = [WeatherResponse(*row) for row in rows]
                    return response
    
    def lowest_temp_per_city(self):
        with self._conn.transaction():
            with self._conn.cursor() as cur:
                
                cur.execute(
                    """SELECT c.city,
                    MIN(w.temp_min_f)
                            FROM weather_analytics.weather w
          	            INNER JOIN weather_analytics.city c
                         	ON c.city_id = w.city_id
          	            GROUP BY c.city"""
                        
                )
                rows = cur.fetchall()
                

                if not rows:
                    print("No records found.")
                    return None
                else:
                    response = [WeatherResponse(*row) for row in rows]
                    return response
    
    
    def total_monthly_precipitation_per_city(self):
        with self._conn.transaction():
            with self._conn.cursor() as cur:
                
                cur.execute(
                    """
                    SELECT
                    DATE_TRUNC('month',w.weather_date) weather_month,
                    c.city,
                    SUM(w.precipitation_sum_in)
                    FROM weather_analytics.weather w
          	        INNER JOIN weather_analytics.city c
                         	ON c.city_id = w.city_id
                    GROUP BY weather_month,c.city
                    ORDER BY c.city ASC ,weather_month ASC;

                    """
                        
                )
                rows = cur.fetchall()

                if not rows:
                    print("No records found.")
                    return None
                else:
                    response = [PrecipResponse(*row) for row in rows]
                    return response
    
    
    def total_hourly_precipitation_per_city(self):
        with self._conn.transaction():
            with self._conn.cursor() as cur:
                
                cur.execute(
                    """
                    SELECT
                    DATE_TRUNC('month',w.weather_date) weather_month,
                    c.city,
                    SUM(w.precipitation_hours)
                    FROM weather_analytics.weather w
          	        INNER JOIN weather_analytics.city c
                         	ON c.city_id = w.city_id
                    GROUP BY weather_month,c.city
                    ORDER BY c.city ASC ,weather_month ASC;

                    """
                        
                )
                rows = cur.fetchall()

                if not rows:
                    print("No records found.")
                    return None
                else:
                    response = [PrecipResponse(*row) for row in rows]
                    return response
    
    
    def windiest_week_per_city(self):
        with self._conn.transaction():
            with self._conn.cursor() as cur:
                
                cur.execute(
                    """
                    SELECT DISTINCT ON (city)
                    city,
                    weather_week,
                    avg_speed
                    FROM (
                        SELECT
                        c.city,
                        DATE_TRUNC('week',w.weather_date)::date weather_week,
                        AVG(w.wind_speed_max_mph) avg_speed
                        FROM weather_analytics.weather w
                                    INNER JOIN weather_analytics.city c
                                                    ON c.city_id = w.city_id
                        GROUP BY c.city, weather_week
                    ) weekly_avg
                    ORDER BY city, avg_speed DESC
                    """

                )
                rows = cur.fetchall()

                if not rows:
                    print("No records found.")
                    return None
                else:
                    response = [WindResponse(*row) for row in rows]
                    return response
    
    