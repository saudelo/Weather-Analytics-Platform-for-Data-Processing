"""script to ingest data from open mateo api
"""
import requests
from pathlib import Path
import os

phoenix_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=33.44838&longitude=-112.07404&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
seattle_url = "https://archive-api.open-meteo.com/v1/archive?latitude=47.60621&longitude=-122.33207&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
chicago_url = "https://archive-api.open-meteo.com/v1/archive?latitude=41.85003&longitude=-87.65005&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
juneau_url =  "https://archive-api.open-meteo.com/v1/archive?latitude=58.30194&longitude=-134.41972&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
miami_url = "https://archive-api.open-meteo.com/v1/archive?latitude=25.77427&longitude=-80.19366&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"


#this is my main function
def get_data():

    file_path = Path.cwd().parent / "data" / "raw_json.json"
    requests.get
    with open(file_path,"w"):
        pass



if __name__ == "__main__":
    get_data()