import pandas as pd
import os

csv_files = [
    "C:/Users/DELL/Desktop/all district/colombo/Colombo_daily.csv",
    "C:/Users/DELL/Desktop/all district/colombo/Ratmalana_daily.csv"
]


# Dictionary to store each station DataFrame
station_data = {}

# List to store all data for combining
all_data_frames = []

# Loop through files
for file in csv_files:
    try:
        print(f"Reading {file}...")
        
        # Read CSV and select needed columns
        df = pd.read_csv(file, usecols=['station_name', 'yyyy', 'mm', 'dd', 'obs'])
        
        # Rename columns so pd.to_datetime works
        df = df.rename(columns={'yyyy': 'year', 'mm': 'month', 'dd': 'day'})
        
        # Create a date column from year, month, day
        df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])
        
        # Drop the original year, month, day columns
        df = df.drop(columns=['year', 'month', 'day'])
        
        # Store in dictionary by station name
        unique_stations = df['station_name'].unique()
        for station in unique_stations:
            station_df = df[df['station_name'] == station].copy()
            station_data[station] = station_df
        
        # Append all data for combining
        all_data_frames.append(df)
    
    except Exception as e:
        print(f"Error reading file {file}: {e}")

# Combine all data
if all_data_frames:
    all_data = pd.concat(all_data_frames, ignore_index=True)
    
    # Save combined data for all stations
    all_data.to_csv('Combined_Rainfall_All_Stations_colombo.csv', index=False)
    
    # Group by Date and get max rainfall
    max_rainfall_per_day = all_data.groupby('Date')['obs'].max().reset_index()
    max_rainfall_per_day.columns = ['Date', 'Max_Rainfall']
    
    # Save max rainfall per day
    max_rainfall_per_day.to_csv('CSV_Extreme_Rainfall_By_Day_colombo.csv', index=False)
    
    print("✅ Combined_Rainfall_All_Stations.csv saved!")
    print("✅ Extreme_Rainfall_By_Day.csv saved!")
else:
    print("⚠️ No valid data loaded — please check your CSV files!")
