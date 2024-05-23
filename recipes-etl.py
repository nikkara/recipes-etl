import json
import pandas as pd

# creation of an empty list to store the JSON objects
recipe_list = []

file_path = "recipes.json"

# Read the file line by line and parse each JSON object
with open(file_path, 'r') as f:
    for jsonObj in f:
            recipe_dict = json.loads(jsonObj.strip())
            recipe_list.append(recipe_dict)

# Convert the list of JSON objects to a DataFrame
df = pd.DataFrame(recipe_list)

# Display the DataFrame
print(df)

# Create a boolean mask for each variation of the word "Chilies"
filtered_df = df[df['ingredients'].str.contains('Chili|Chilies|Chile|Chili|Chiles', case=False)]

# Calculate the time deltas out of ISO 8601
filtered_df['cookTime_timedelta'] = pd.to_timedelta(filtered_df['cookTime'], errors='coerce')
filtered_df['prepTime_timedelta'] = pd.to_timedelta(filtered_df['prepTime'], errors='coerce')

# Convert to seconds
filtered_df['cookTime_seconds'] = filtered_df['cookTime_timedelta'].dt.total_seconds()
filtered_df['prepTime_seconds'] = filtered_df['prepTime_timedelta'].dt.total_seconds()

# Calculate total cook times
filtered_df['total_cook_time'] = filtered_df['cookTime_seconds']+filtered_df['prepTime_seconds']

# Add Dificulties based on cook time
filtered_df['time_classification'] = filtered_df['total_cook_time'].apply(lambda x: 'Hard' if x >3600  else ('Medium' if 1800 < x <= 3600 else ('Easy' if 0 < x <= 1800 else 'Unknown')))

# Drop the specified columns
filtered_df = filtered_df.drop(['cookTime_timedelta','prepTime_timedelta','cookTime_seconds','prepTime_seconds','total_cook_time'], axis=1)

# Export to csv
filtered_df.to_csv('chilies_recipes.csv')