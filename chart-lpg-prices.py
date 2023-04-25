import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('lpg-historical-prices-iocl.xlsx')

df['Month'] = pd.to_datetime(df['Month'])

# Replace 'No Change' with NaN values in the 'Price' column
df['Delhi'] = df['Delhi'].replace('No Change', np.nan)
# Convert the 'Price' column from text to numeric values
df['Delhi'] = pd.to_numeric(df['Delhi'], errors='coerce')


df['Mumbai'] = df['Mumbai'].replace('No Change', np.nan)
df['Mumbai'] = pd.to_numeric(df['Mumbai'], errors='coerce')

df['Kolkata'] = df['Kolkata'].replace('No Change', np.nan)
df['Kolkata'] = pd.to_numeric(df['Kolkata'], errors='coerce')

df['Chennai'] = df['Chennai'].replace('No Change', np.nan)
df['Chennai'] = pd.to_numeric(df['Chennai'], errors='coerce')

df_yearly = df.groupby(df['Month'].dt.year).mean()

# Set the 'Month' column as the index of the DataFrame
df = df.set_index('Month')

# Create a time series plot using matplotlib
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df.index, df['Delhi'], label='Delhi')
ax.bar(df.index, df['Kolkata'], label='Kolkata')
ax.bar(df.index, df['Mumbai'], label='Mumbai')
ax.bar(df.index, df['Chennai'], label='Chennai')

# Add labels and title to the plot
ax.set_xlabel('Month')
ax.set_ylabel('Price (Rs.)')
ax.set_title('LPG Prices')

# Add a legend to the plot
ax.legend()

# Save the plot to your working directory
plt.savefig('chart.png', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()