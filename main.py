#script to orchestrate pipeline
#import dependencies
# from dao.city_dao import create_city_table
# from dao.weather_dao import create_weather_table
from db_util.db_util import get_conn_string
from datetime import datetime
from pathlib import Path
import psycopg

from transform.analyze_data import analyze_data
from dao.weather_dao import WeatherDAO
from dao.city_dao import CityDAO
CITY = "City"
WEATHER = "Weather"
def main():

    #ingest data

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

