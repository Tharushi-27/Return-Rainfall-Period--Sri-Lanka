import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genpareto
import os

# List of your CSV files
csv_files = [
    "C:/Users/DELL/Desktop/all district/colombo/Colombo_daily.csv",
    "C:/Users/DELL/Desktop/all district/colombo/Ratmalana_daily.csv"
]

# GPD threshold (percentile)
threshold_percentile = 95

# Initialize the plot
plt.figure(figsize=(12, 8))
colors = plt.colormaps.get_cmap('tab20')

# Loop through files
for i, file in enumerate(csv_files):
    # Load CSV
    df = pd.read_csv(file)

    # Extract daily rainfall
    rainfall = df['obs'].dropna()

    # Calculate threshold for extreme values
    threshold = np.percentile(rainfall, threshold_percentile)

    # Select extreme values above threshold
    excesses = rainfall[rainfall > threshold] - threshold

    # Fit GPD
    params = genpareto.fit(excesses)

    # Define return periods (years)
    return_periods = np.logspace(0.1, 2.5, 100)  # ~1.25 to ~300 years

    # Number of exceedances
    n_exceedances = len(excesses)
    n_total = len(rainfall)

    # Annual exceedance probability
    p_exceed = n_exceedances / n_total

    # GPD parameters
    shape, loc, scale = params

    # Return levels
    return_levels = threshold + (scale / shape) * ((return_periods * p_exceed) ** shape - 1)

    # Remove negatives
    return_levels = np.maximum(return_levels, 0)

    # Label
    if 'station_name' in df.columns:
        station_label = df['station_name'].iloc[0]
    else:
        station_label = os.path.splitext(os.path.basename(file))[0]

    # Plot
    plt.plot(return_periods, return_levels, label=station_label, color=colors(i / len(csv_files)))

# Plot formatting

plt.title("Return Rainfall Observations at Multiple Stations - Ratnapura")
plt.xlabel("Return Period (years)")
plt.ylabel("Rainfall (mm)")
plt.grid(True, which='both', linestyle='--')
plt.legend(title="Station", fontsize='small', ncol=2)
plt.tight_layout()

# Show plot
plt.show()


