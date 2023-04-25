import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the URL to scrape
url = 'https://iocl.com/indane-14Kg-nonsubsid-previous-price'

# Use pandas to read the table from the URL
dfs = pd.read_html(url)

# Select the first table from the list of tables
df = dfs[0]

# Save the table to an Excel file
df.to_excel('lpg-historical-prices-iocl.xlsx', index=False)

###

