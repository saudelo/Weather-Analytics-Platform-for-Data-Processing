import json
import pandas as pd
from pathlib import Path

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


# Unpacking multiple list columns into individual columns
#df[['col1', 'col2']] = df.apply(lambda row: pd.Series([row['list_col1'], row['list_col2']]), axis=1)

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

print(city_df)


#Next creating my subset of data for weather data. 
#weather_df = df[["city_id",]].drop_duplicates()

# Replace strings
#df = df.replace(['N/A, 'null', 'None', ''], sting_to_put)

#drop unecessary columns after creating subset of city data
#df = df.drop(columns=columns_to_remove, errors='ignore')

""" file_path_normalized = Path.cwd() / "data" / "normalized_weather.json"
weather_df.to_json(file_path_normalized, orient="records", indent=4) """

   



