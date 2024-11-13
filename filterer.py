import pandas as pd

# Load the CSV file
file_path = 'Port_vs_Spain2_audio.csv'
data = pd.read_csv(file_path)

# Clean 'Timestamp' column by removing trailing ".00" and convert to numeric
data['Timestamp'] = data['Timestamp'].astype(str).str.replace(r'\.00$', '', regex=True)
data['Timestamp'] = pd.to_numeric(data['Timestamp'], errors='coerce')

# Drop rows with null values in 'Timestamp' after conversion
data.dropna(subset=['Timestamp'], inplace=True)

# Filter rows where 'Event Category' is 'Goals and Scoring Opportunities'
filtered_data = data[data['Event Category'] == 'Goals and Scoring Opportunities']

# Sort by 'Timestamp' to ensure events are in chronological order
filtered_data = filtered_data.sort_values(by='Timestamp').reset_index(drop=True)

# Drop repeated events within the same minute by ensuring at least 1 minute difference
filtered_data = filtered_data[filtered_data['Timestamp'].diff().fillna(float('inf')) > 1]

# Reset index after filtering
filtered_data.reset_index(drop=True, inplace=True)

# Display the filtered data
# print(filtered_data)

# Save the filtered data to a new CSV if needed
filtered_data.to_csv(file_path, index=False)
