import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genpareto

# Load data
df = pd.read_csv("C:/Users/DELL/Desktop/all district/ratnapura/CSV_GODAKAWELA.csv")
df['obs'] = pd.to_numeric(df['obs'], errors='coerce')
df.dropna(subset=['obs'], inplace=True)

# Step 1: Choose a high threshold (e.g., 100 mm)
threshold = 100
exceedances = df[df['obs'] > threshold]['obs'] - threshold

# Step 2: Fit Generalized Pareto Distribution (GPD)
shape, loc, scale = genpareto.fit(exceedances, floc=0)  # location fixed at 0

print(f"GPD Parameters:\nShape (ξ): {shape:.4f}, Scale (σ): {scale:.2f}")

# Total number of years in your data
n_years = df['yyyy'].nunique()

# Number of exceedances
n_exceed = len(exceedances)

# Exceedance rate (per year)
lambda_exceed = n_exceed / n_years

# Define rainfall levels above the threshold
rainfall_levels = np.array([100, 150, 200, 250,300,350,400])  # in mm
x = rainfall_levels - threshold  # adjust to GPD scale

# Calculate return periods
cdf_vals = genpareto.cdf(x, shape, loc=0, scale=scale)
return_periods = 1 / (lambda_exceed * (1 - cdf_vals))

for r, t in zip(rainfall_levels, return_periods):
    print(f"Rainfall {r} mm → Return Period ≈ {t:.2f} years")

plt.plot(rainfall_levels, return_periods, marker='o')
plt.xlabel("Rainfall (mm)")
plt.ylabel("Return Period (years)")
plt.title("Return Period vs Rainfall - Godakawela (POT-GPD Method)")
plt.grid(True)
plt.show()
