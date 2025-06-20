import pandas as pd
import os

# List of your CSV files
csv_files = [
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_ALUPOLA.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_CARNEY ESTATE.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_CHANDRIKAWEWA.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_DEPEDENA GROUP.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_DETANAGALLA.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_EHELIYAGODA S.P..csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_EMBILIPITIYA.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_GALATURA ESTATE.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_GILIMALAY ESTATE.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_GODAKAWELA.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_HALLAYEN ESTATE.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_MUTWAGALLA ESTATE.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_non pariel.csv",
    "C:/Users/DELL/Desktop/all district/ratnapura/CSV_RASSAGALA.csv"
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
    all_data.to_csv('Combined_Rainfall_All_Stations_ratnapura.csv', index=False)
    
    # Group by Date and get max rainfall
    max_rainfall_per_day = all_data.groupby('Date')['obs'].max().reset_index()
    max_rainfall_per_day.columns = ['Date', 'Max_Rainfall']
    
    # Save max rainfall per day
    max_rainfall_per_day.to_csv('CSV_Extreme_Rainfall_By_Day_ratnapura.csv', index=False)
    
    print("✅ Combined_Rainfall_All_Stations.csv saved!")
    print("✅ Extreme_Rainfall_By_Day.csv saved!")
else:
    print("⚠️ No valid data loaded — please check your CSV files!")
