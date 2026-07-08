from psycopg.rows import dict_row
from dataclasses import dataclass
from typing import Optional

@dataclass
class CityRecord:
    city_id: int
    city: str
    longitude: float
    latitude: float
    us_state: str



## =============================================================================
# DAO CLASS
# -`bulk_create(city, longitude,latitude,us_state)` — insert records into city table in bulk
# =============================================================================

class CityDAO:
    def __init__(self,conn):
            # Connection string is built once at instantiation from environment
            # variables loaded by db_util in main. All methods reuse this value.
            self._conn = conn

    def _map_row(self, row) -> CityRecord:
            # Private helper that converts a psycopg Row (dict-style) into an
            # dataclass instance.

            return CityRecord(
                city_id=row["city_id"],
                city=row["city"],
                longitude=row["longitude"],
                latitude=row["latitude"],
                us_state=row["us_state"]
            )
    def create(self,city_df):
        data_to_insert = list(city_df.itertuples(index=False, name=None))
        with self._conn.transaction():
              with self._conn.cursor() as cur:
                    cur.execute(
                          "TRUNCATE TABLE weather_analytics.city"
                    )
                    cur.executemany(
                        "INSERT INTO weather_analytics.city (city_id,city_name,longitude,latitude,us_state) VALUES (%s, %s, %s, %s, %s)", 
                        data_to_insert)
                    return cur.rowcount