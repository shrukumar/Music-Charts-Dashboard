import plotly.express as px
import pandas as pd
"""Visualization 2:
Histogram that shows how many songs are released per month (year does not matter)
Component 1: Slider/date picker of range
Component 2: months or days 
Released month / day / streams 
"""
csv = 'spotify-2023.csv'
# csv = 'test.csv'

df_song = pd.read_csv(csv)
print(df_song.head())


# fig = px.histogram(df, x="total_bill")
# fig.show()