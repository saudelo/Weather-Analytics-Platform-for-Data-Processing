#script to orchestrate pipeline
#import dependencies
from db_util.db_util import get_conn_string
from datetime import datetime
from pathlib import Path
import psycopg

#ingest data

#call transformation script

#create a connection to the database
def main():
    with psycopg.connect(get_conn_string()) as conn:
        intialize_db(conn)






#helper function
def intialize_db(conn):
    """Initialize the database"""
    
    """     script_dir = os.path.dirname(os.path.abspath(__file__))
    ddl_path = os.path.join(script_dir, "ddl.sql") """
    try:
        with conn.transaction():
            with open(ddl_path,"r") as file:
                sql = file.read()
                with conn.cursor() as cur:
                    cur.execute(sql)
                    print("Setup successful")
                              
    except psycopg.Error as e:
        print(f"Database Setup Failed - Exception thrown: {e}")


#and load the data into the database


#call sql queries on data

