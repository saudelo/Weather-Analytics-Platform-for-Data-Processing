"""script to ingest data from open mateo api
"""
import json
import time
import requests
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import sys

TIMEOUT=5   #timeout in seconds for the requests

#will move these urls to a config file later
PHOENIX_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=33.44838&longitude=-112.07404&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
SEATTLE_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=47.60621&longitude=-122.33207&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
CHICAGO_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=41.85003&longitude=-87.65005&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
JUNEAU_URL =  "https://archive-api.open-meteo.com/v1/archive?latitude=58.30194&longitude=-134.41972&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
MIAMI_URL = "https://archive-api.open-meteo.com/v1/archive?latitude=25.77427&longitude=-80.19366&start_date=2024-01-01&end_date=2024-12-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum,precipitation_hours&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"

_count = 0
#this is my main function
def get_data():

    retry_strategy = Retry(
    total=3, #total retries
    backoff_factor=.2, #wait time between retries
    status_forcelist=[500, 503], #retry on these status codes
    raise_on_status=True #raises an exception if the request fails after the specified number of retries
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    try:
        file_path = Path.cwd() / "data" / "raw_data.json"
        
        with requests.Session() as session:
            session.mount("https://", adapter)
            session.hooks = {'response': handle_rate_limit}

            response_phx = session.get(PHOENIX_URL, timeout=TIMEOUT)
            response_seattle = session.get(SEATTLE_URL, timeout=TIMEOUT)
            response_chicago = session.get(CHICAGO_URL, timeout=TIMEOUT)
            response_juneau = session.get(JUNEAU_URL, timeout=TIMEOUT)
            response_miami = session.get(MIAMI_URL, timeout=TIMEOUT)

            # Write the response JSON data to a file
            with open(file_path,"w") as f:
                f.write("[")  # Start of the JSON array
                json.dump(response_phx.json(), f, indent=4)
                f.write(",")  # Add a comma between JSON objects
                json.dump(response_seattle.json(), f, indent=4)
                f.write(",")  # Add a comma between JSON objects
                json.dump(response_chicago.json(), f, indent=4)
                f.write(",")  # Add a comma between JSON objects
                json.dump(response_juneau.json(), f, indent=4)
                f.write(",")  # Add a comma between JSON objects
                json.dump(response_miami.json(), f, indent=4)
                f.write("]")  # End of the JSON array

    except FileNotFoundError as e:
        print(f"File not found in {file_path}: {e}")
    except requests.exceptions.RetryError as e:
        print(f"Request failed after max 3 retries: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.HTTPError as e:  #returns 400 if url not specified correctly
        if e.response.status_code == 400:
            print(f"HTTP error 400: Bad Request. Please check the URL. Error: {e}")
        elif e.response.status_code == 429:
            print(f"HTTP error 429: Too Many Requests. Rate limit exceeded. Error: {e}")
        else:
            print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Other request error: {e}")


def handle_rate_limit(response,*args, **kwargs):
    
    if response.status_code == 429:
        retry_val = response.headers.get("Retry-After")
        retry_val = int(retry_val) if retry_val else None
        if retry_val and retry_val == 60:
            print("Rate limit exceeded. Waiting 60 seconds before retrying...")
            time.sleep(retry_val)
            new_response = response.connection.send(response.request)
            return handle_rate_limit(new_response) #will loop through one more time to check there is no 429 error
        elif retry_val and retry_val > 60:
            print("Max daily limit reached. Exiting.")
            sys.exit(1)  
        else:
            time.sleep(0.2)

    response.raise_for_status()  # Raises an exception for other HTTP errors not already handledwith every call to the API
    return response

if __name__ == "__main__":
    get_data()