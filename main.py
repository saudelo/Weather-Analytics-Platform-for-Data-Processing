#script to orchestrate pipeline
#import dependencies
# from dao.city_dao import create_city_table
# from dao.weather_dao import create_weather_table
from db_util.db_util import get_conn_string
from datetime import datetime
from pathlib import Path
import psycopg


def main():

    #ingest data

    #call transformation script

    #create a connection to the database

    with psycopg.connect(get_conn_string()) as conn:
        intialize_db(conn)


    #and load the data into the database

    #call sql queries on data


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
                              
    except psycopg.Error as e:
        print(f"Database Setup Failed - Exception thrown: {e}")


if __name__ == "__main__":
    main()

