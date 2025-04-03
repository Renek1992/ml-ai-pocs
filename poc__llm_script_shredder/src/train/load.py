
import pandas as pd
import glob
import json

json_files = glob.glob('results/*.json')


# Path pattern for JSON files (adjust as needed)
file_pattern = 'results/*.json'

# List to hold the content of each JSON file
combined_data = []

# Iterate over all JSON files matching the pattern
for file_name in glob.glob(file_pattern):
    with open(file_name, 'r') as file:
        data = json.load(file)
        combined_data.append(data)

# Write combined data to a new JSON file
with open('final/training_dataset.json', 'w') as output_file:
    json.dump(combined_data, output_file, indent=4)
