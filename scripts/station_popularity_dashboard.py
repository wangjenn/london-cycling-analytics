# Creating dashboard for Station Popularity using Plotly in Python 

import os 
import pandas as pd 
import requests 
import time 
import logging 
from concurrent.futures import ThreadPoolExecutor 
from datetime import datetime 
import numpy as np 
import matplotlib
import glob
import pprint
import re
import plotly
from google.cloud import bigquery
from google.cloud import storage
import matplotlib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

client = bigquery.Client()

# Read in query
query = """SELECT *
FROM `london_cycles.station_popularity`
ORDER BY total_traffic DESC 
LIMIT 15 """

station = client.query(query).to_dataframe()
station

# Format the DataFrame with styling
def color_net_flow(val):
    """Apply red for negative flow, green for positive flow"""
    color = 'red' if val < 0 else 'green' if val > 0 else 'black'
    return f'color: {color}'

styled_df = station.style.format({
    'total_starts': '{:,}',
    'total_ends': '{:,}',
    'total_traffic': '{:,}',
    'net_flow': '{:+,}'  # Plus sign shows direction
}).applymap(color_net_flow, subset=['net_flow']
).background_gradient(subset=['total_traffic'], cmap='Blues'
).set_caption('London Bicycle Station Popularity')

# Display in notebook
styled_df


# Total Traffic
# Create DataFrame from your data
data = {
    'station_id': [191, 1075, 1072, 213, 303, 2696, 194, 2587, 307, 785, 960, 1161, 300083, 111, 1132],
    'station_name': [
        'Hyde Park Corner, Hyde Park', 'Hyde Park Corner, Hyde Park', 'Waterloo Station 3, Waterloo',
        'Wellington Arch, Hyde Park', 'Albert Gate, Hyde Park', 'Waterloo Station 1, Waterloo',
        'Hop Exchange, The Borough', 'Wormwood Street, Liverpool Street', 'Black Lion Gate, Kensington Gardens',
        'Aquatic Centre, Queen Elizabeth Olympic Park', 'Hop Exchange, The Borough',
        'Brushfield Street, Liverpool Street', 'Duke Street Hill, London Bridge',
        'Park Lane , Hyde Park', 'Albert Gate, Hyde Park'
    ],
    'total_starts': [30860, 28073, 26003, 23126, 21202, 21311, 18002, 19931, 19303, 19307, 16804, 16341, 17707, 17585, 17283],
    'total_ends': [31084, 26883, 27936, 23054, 21293, 20711, 22878, 20020, 19479, 19464, 21730, 21260, 19121, 17834, 17146],
    'total_traffic': [61944, 54956, 53939, 46180, 42495, 42022, 40880, 39951, 38782, 38771, 38534, 37601, 36828, 35419, 34429],
    'net_flow': [-224, 1190, -1933, 72, -91, 600, -4876, -89, -176, -157, -4926, -4919, -1414, -249, 137]
}

df = pd.DataFrame(data)

# 1. Top Stations by Total Traffic
fig1 = px.bar(
    df.sort_values('total_traffic', ascending=False),
    x='station_name',
    y='total_traffic',
    title='Top 15 Bicycle Stations by Total Traffic',
    labels={'total_traffic': 'Total Trips', 'station_name': 'Station Name'}
)

fig1.update_layout(
    xaxis_tickangle=-45,
    height=600,
    width=1000
)

fig1.write_html('station_popularity.html')
fig1.show()


# 2. Station Starts vs. Ends 
df_melted = pd.melt(
    station, 
    id_vars=['station_name', 'station_id'],
    value_vars=['total_starts', 'total_ends'],
    var_name='trip_type',
    value_name='trips'
)

fig2 = px.bar(
    df_melted.sort_values(by=['trips'], ascending=False),
    x='station_name',
    y='trips',
    color='trip_type',
    title='Station Usage Composition: Starts vs. Ends',
    labels={'trips': 'Number of Trips', 'station_name': 'Station Name', 'trip_type': 'Trip Type'},
    color_discrete_map={'total_starts': 'royalblue', 'total_ends': 'lightcoral'},
    barmode='group'
)

fig2.update_layout(
    xaxis_tickangle=-45,
    height=600,
    width=1000,
    legend_title_text='Trip Type'
)

fig2.write_html('station_composition.html')
fig2.show()

# 3. Netflow 
# 3. Station Net Flow
fig3 = px.bar(
    station.sort_values('net_flow'),
    x='station_name',
    y='net_flow',
    color='net_flow',
    color_continuous_scale='RdBu',
    title='Station Net Flow (Starts minus Ends)',
    labels={'net_flow': 'Net Flow', 'station_name': 'Station Name'}
)

fig3.update_layout(
    xaxis_tickangle=-45,
    height=600,
    width=1000
)

# Add a reference line at y=0
fig3.add_shape(
    type="line",
    x0=-0.5,
    y0=0,
    x1=len(station)-0.5,
    y1=0,
    line=dict(color="black", width=1, dash="dash")
)

fig3.write_html('station_net_flow.html')
fig3.show()

# 4. Top 5 Origin (Start) and End (Destination) Stations
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 4. Create comprehensive dashboard showing station types
# Group stations by area
df = station
df['area'] = df['station_name'].apply(lambda x: x.split(',')[-1].strip())

# Create a figure with 2 subplots
fig4 = make_subplots(
    rows=2, cols=1,
    subplot_titles=(
        'Top 5 Origin Stations (Positive Net Flow)',
        'Top 5 Destination Stations (Negative Net Flow)'
    ),
    vertical_spacing=0.15,
    specs=[[{"type": "bar"}], [{"type": "bar"}]]
)

# Top origin stations (positive net flow)
origin_stations = df[df['net_flow'] > 0].sort_values('net_flow', ascending=False).head(5)
fig4.add_trace(
    go.Bar(
        x=origin_stations['station_name'],
        y=origin_stations['net_flow'],
        marker_color='royalblue',
        text=origin_stations['net_flow'],
        textposition='auto',
        name='Net Outflow'
    ),
    row=1, col=1
)

# Top destination stations (negative net flow)
destination_stations = df[df['net_flow'] < 0].sort_values('net_flow').head(5)
fig4.add_trace(
    go.Bar(
        x=destination_stations['station_name'],
        y=destination_stations['net_flow'].abs(),
        marker_color='lightcoral',
        text=destination_stations['net_flow'].abs(),
        textposition='auto',
        name='Net Inflow'
    ),
    row=2, col=1
)

# Update layout
fig4.update_layout(
    height=800,
    width=1000,
    title_text="London Bicycle Station Flow Patterns",
    showlegend=True
)

fig4.update_xaxes(tickangle=-45, row=1, col=1)
fig4.update_xaxes(tickangle=-45, row=2, col=1)

fig4.write_html('station_types.html')
fig4.show()
