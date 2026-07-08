import json
import pandas as pd
from pathlib import Path

def analyze_data():
    file_path = Path.cwd() / "data" / "raw_data.json"
    # loading the JSON file
    with open(file_path, 'r') as file:
        raw_data = json.load(file)

    # normalize the data
    df = pd.json_normalize(raw_data)


    #exploring data and missing values
    print(f"Shape: {df.shape[0]} rows and {df.shape[1]} columns")
    print(f"Column names: {df.columns.tolist()}")
    print(f"data types: {df.dtypes.tolist()}")

    print(f"Getting info: {df.info()}")

    #inspecting for
    #Null or missing values
    #Type inconsistencies
    #Unexpected value ranges
    #Duplicate records

    print("Missing values per column:")
    print(df.isnull().sum())


    #Checking for duplicates
    def make_hashable(val):
        try:
            hash(val)
            return val  # It's already hashable (strings, numbers, tuples)
        except TypeError:
            if isinstance(val, (list, set)):
                return tuple(val)
            if isinstance(val, dict):
                # Sort items so {a:1, b:2} matches {b:2, a:1}
                return tuple(sorted(val.items())) 
            return str(val)  # Fallback for anything else unusual

    # Apply hashable function safely across whole DataFrame copy
    df_hashable = df.copy()
    df_hashable = df_hashable.map(make_hashable)
    print(f"\nDuplicate rows: {df_hashable.duplicated().sum()}")

    #no need to drop duplicates or missing values since there are none.

    # Check for missing values total in all columns
    missing_total = df.isnull().sum().sum()

    print(f"Total missing values: {missing_total}")

    #Finished exploration of data and missing values.
    #adding city_id to the main dataframe to more easily isolate city_data
    df.loc[(df['latitude'] == 33.427063) & (df['longitude'] == -112.02719), 'city_id'] = 1
    df.loc[(df['latitude'] == 47.627415) & (df['longitude'] == -122.32291), 'city_id'] = 2
    df.loc[(df['latitude'] == 41.862915) & (df['longitude'] == -87.648770), 'city_id'] = 3
    df.loc[(df['latitude'] == 58.242530) & (df['longitude'] == -134.40788), 'city_id'] = 4
    df.loc[(df['latitude'] == 25.764498) & (df['longitude'] == -80.196075), 'city_id'] = 5

    df['city_id'] = df['city_id'].astype(int)
    # Now creating a subset of data called city_data
    city_df = df[["city_id","latitude", "longitude"]].drop_duplicates()

    city_df.loc[(city_df['city_id'] == 1), 'city'] = "Phoenix"
    city_df.loc[(city_df['city_id'] == 1), 'us_state'] = "Arizona"

    city_df.loc[(city_df['city_id'] == 2), 'city'] = "Seattle"
    city_df.loc[(city_df['city_id'] == 2), 'us_state'] = "Washington"

    city_df.loc[(city_df['city_id'] == 3), 'city'] = "Chicago"
    city_df.loc[(city_df['city_id'] == 3), 'us_state'] = "Illinois"

    city_df.loc[(city_df['city_id'] == 4), 'city'] = "Juneau"
    city_df.loc[(city_df['city_id'] == 4), 'us_state'] = "Alaska"

    city_df.loc[(city_df['city_id'] == 5), 'city'] = "Miami"
    city_df.loc[(city_df['city_id'] == 5), 'us_state'] = "Florida"
    city_df = city_df[["city_id","city","longitude","latitude","us_state"]]
    print(city_df)

    #renaming weather data columns to match the database schema
    df = df.rename(columns={'daily.time': 'weather_date',
                            'daily.temperature_2m_mean': 'temp_mean_f',
                            'daily.temperature_2m_max': 'temp_max_f', 
                            'daily.temperature_2m_min': 'temp_min_f',
                            'daily.precipitation_sum': 'precipitation_sum_in',
                            'daily.precipitation_hours': 'precipitation_hours',
                            'daily.wind_speed_10m_max': 'wind_speed_max_mph'})

    #Next creating my subset of data for weather data. 
    weather_df = df[["city_id", "weather_date", "temp_mean_f", "temp_max_f", "temp_min_f", "precipitation_sum_in", "precipitation_hours", "wind_speed_max_mph"]]

    #exploding lists to turn into tabular data
    weather_df = weather_df.explode(['weather_date', 'temp_mean_f','temp_max_f', 'temp_min_f','precipitation_sum_in', 'precipitation_hours', 'wind_speed_max_mph'], ignore_index=True)

    #preview
    print(weather_df.head())


    #check data for inconsistencies and missing values after exploding lists

    #max greater than min check
    max_greater_than_min = (weather_df['temp_max_f'] < weather_df['temp_min_f']).any()
    if max_greater_than_min: #if at least one row has max less than min, print a warning
        print("Warning: There are rows where temp_max_f is less than temp_min_f.")
        weather_df.loc[weather_df['temp_max_f'] < weather_df['temp_min_f'], 'temp_max_f'] = None
        weather_df.loc[weather_df['temp_min_f'] > weather_df['temp_max_f'], 'temp_min_f'] = None
        weather_df['temp_min_f','temp_max_f'] = weather_df.groupby('city_id')['temp_min_f','temp_max_f'].ffill()

    # check impossible placeholder temperatures
    weather_temp_error_max = (weather_df['temp_max_f'] > 140).any()
    if weather_temp_error_max:
        print("Warning: There are rows where temp_max_f is greater than 140°F, which is an impossible value.")
        weather_df.loc[weather_df['temp_max_f'] > 140, 'temp_max_f'] = None
        weather_df['temp_max_f'] = weather_df.groupby('city_id')['temp_max_f'].ffill()

    weather_temp_error_min = (weather_df['temp_min_f'] < -130).any()
    if weather_temp_error_min:
        print("Warning: There are rows where temp_min_f is less than -130°F, which is an impossible value.")
        weather_df.loc[weather_df['temp_min_f'] < -130, 'temp_min_f'] = None
        weather_df['temp_min_f'] = weather_df.groupby('city_id')['temp_min_f'].ffill()



    #ensuring there are only unique rows for each city_id and weather_date combination after exploding lists
    duplicate_count = weather_df.duplicated(subset=['city_id', 'weather_date']).sum()
    print(f"Total duplicate rows after normalization/transformation: {duplicate_count}")

    #recheck missing columns after exploding lists
    missing_total_normalized = weather_df.isnull().sum().sum()
    print(f"Total missing values after normalization/transformation: {missing_total_normalized}")

    """ 
    #for testing purposes, saving the normalized data to a JSON file
    file_path_normalized = Path.cwd() / "data" / "normalized_weather.json"
    weather_df.to_json(file_path_normalized, orient="records", indent=4) """

    return (city_df,weather_df)

if __name__ == "__main__":
    analyze_data()