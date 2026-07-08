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
    def create(weather_df):
             pass

