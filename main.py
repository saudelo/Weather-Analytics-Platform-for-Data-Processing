#script to orchestrate pipeline
#import dependencies
# from dao.city_dao import create_city_table
# from dao.weather_dao import create_weather_table
from db_util.db_util import get_conn_string
from datetime import datetime
from pathlib import Path
import psycopg

from transform.analyze_data import analyze_data
from ingestion.fetch_data import get_data
from dao.weather_dao import WeatherDAO
from dao.city_dao import CityDAO
CITY = "City"
WEATHER = "Temperature in F"
PRECIP_SUM = "Inches of Precipitation"
MONTH = "Month"
PRECIP_HOURS = "Hours of Precipitation"
WEEK = "Week"
WIND_SPEED = "Avg Wind Speed"
def main():


    #ingest data and save to raw JSON file
    get_data()

    #call transformation script
    city_df,weather_df = analyze_data()

    #create a connection to the database
    with psycopg.connect(get_conn_string()) as conn:
        intialize_db(conn)
        city_dao = CityDAO(conn)
        weather_dao = WeatherDAO(conn)

        #load the data into the database
        city_row_count = city_dao.create(city_df)
        if city_row_count > 4:
            print(f"Successfully inserted {city_row_count} rows into the database.")
        else:
            print(f"Error inserting rows into city table. Row count is {city_row_count}")
        
        weather_row_count = weather_dao.create(weather_df)
        if weather_row_count > 50:
            print(f"Successfully inserted {weather_row_count} into the database.")
        else:
            print(f"Error inserting rows into weather table. Row count is {weather_row_count}")


        #call sql queries on data
        #Query 1
        response_list = weather_dao.highest_temp_per_city()  #returning list of dataclass for type safety
        print("\nMax Weather per City:\n")
        print(f"{CITY:<10}{WEATHER:<10}")
        print("-----------------------")

        for record in response_list:
            print(f"{record.city_name:<10} {record.weather:<10}")

        #Query 2
        response_list2 = weather_dao.lowest_temp_per_city()  #returning list of dataclass for type safety
        print("\nMin Weather per City:\n")
        print(f"{CITY:<10}{WEATHER:<10}")
        print("-----------------------")

        for record in response_list2:
            print(f"{record.city_name:<10} {record.weather:<10}")

        #Query 3
        response_list3 = weather_dao.total_monthly_precipitation_per_city()  #returning list of dataclass for type safety
        print("\nTotal Monthly Inches of Precipitation By City:\n")
        print(f"{MONTH:<10}{CITY:<10}{PRECIP_SUM:<10}")
        print("-----------------------------------------------------")

        for record in response_list3:
            print(f"{record.weather_date.month:<10}{record.city_name:<10} {f'{record.precip:^15.2f}':>20}")
        

        #Query 4
        response_list4 = weather_dao.total_hourly_precipitation_per_city()  #returning list of dataclass for type safety
        print("\nTotal Monthly Hours of Precipitation By City:\n")
        print(f"{MONTH:<10}{CITY:<10}{PRECIP_HOURS:<10}")
        print("-----------------------------------------------------")

        for record in response_list4:
            print(f"{record.weather_date.month:<10}{record.city_name:<10} {f'{record.precip:^15.1f}':>20}")
        

        #Query 5
        # city_name: str
        # windiest_week: date
        # wind_speed: float

        response_list5 = weather_dao.windiest_week_per_city()  #returning list of dataclass for type safety
        print("\nWindiest Week of the Year By City:\n")
        #Took the average Max wind speed throughout the week and then took the max per city
        print(f"{CITY:<10}{WEEK:<10}{WIND_SPEED:<10}")
        print("-----------------------------------------------------")

        for record in response_list5:
            print(f"{record.city_name:<10}{record.windiest_week.isoformat:<10} {f'{record.wind_speed:^15.2f}':>20}")
    

   


#helper function
def intialize_db(conn):
    """Initialize the database"""
    
    ddl_path = Path.cwd() / "sql" / "weather_analytics_schema.sql"
    try:
        with conn.transaction():
            with open(ddl_path,"r") as file:
                sql = file.read()
                with conn.cursor() as cur:
                    cur.execute(sql)
                    print("Setup successful")
    
    except FileNotFoundError:
        print(f"Database Setup Failed - File not found: {ddl_path}")                          
    except psycopg.Error as e:
        print(f"Database Setup Failed - Exception thrown: {e}")


if __name__ == "__main__":
    main()

