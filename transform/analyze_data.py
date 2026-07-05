import json
import pandas as pd
from pathlib import Path

file_path = Path.cwd() / "data" / "raw_data.json"
# loading the JSON file
with open(file_path, 'r') as file:
    raw_data = json.load(file)

# 2. Flatten/normalize the data
df = pd.json_normalize(raw_data)