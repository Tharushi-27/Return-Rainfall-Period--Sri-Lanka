import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genpareto

# Load data
df = pd.read_csv('C:/Users/DELL/Desktop/all district/CSV_Extreme_Rainfall_By_Day_colombo.csv')

# Use 'Max_Rainfall' column
rainfall = df['Max_Rainfall']


u = 50  # example threshold in mm — change based on your data

# Exceedances over threshold
exceedances = rainfall[rainfall > u] - u

# Fit GPD to exceedances
shape, loc, scale = genpareto.fit(exceedances, floc=0)

print(f'Fitted GPD parameters: shape={shape:.4f}, scale={scale:.4f}')

# Total number of data points
N = len(rainfall)

# Number of exceedances
n_exc = len(exceedances)

# Assume daily data → number of years = N / 365.25
n_years = N / 365.25

# Return periods in years
T = np.logspace(0.1, 3, 50)  # From ~1 year to 1000 years

# Compute return levels (rainfall mm)
if abs(shape) > 1e-6:
    return_levels = u + (scale / shape) * ( (T * n_exc / n_years) ** shape - 1 )
else:  # shape → 0 (Gumbel)
    return_levels = u + scale * np.log( T * n_exc / n_years )

# Plot Return Period Graph
plt.figure(figsize=(10, 6))
plt.plot(return_levels, T, marker='o', linestyle='-', color='pink')
plt.xlabel('Rainfall (mm)')
plt.ylabel('Return Period (Years)')
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.title('Return Period vs Rainfall for ratnapura District using daily rainfall (1991-2025) ')
plt.show()
