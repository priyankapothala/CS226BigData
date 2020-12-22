import pandas as pd
import numpy as np

df = pd.read_csv('Datasets/cities.csv')

print(df.head())

df['pollution_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['rent_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['property_price_to_income_ratio'].interpolate(method='linear', direction = 'forward', inplace=True)
df['health_care_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['traffic_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['crime_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['safety_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df['cpi_index'].interpolate(method='linear', direction = 'forward', inplace=True)
df.to_csv('Datasets/cities_new.csv',index=False)