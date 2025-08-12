import csv
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

pink_dash = Dash(__name__, assets_folder='../assets')

sales = []
date = []
region = []

with open('data/pink_morsels_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sales.append(float(row['sales']))
        date.append(row['date'])
        region.append(row['region'])

# Create the DataFrame
df = pd.DataFrame({
    "Sales": sales,
    "Date": pd.to_datetime(date),
    "Region": region
})

# Define the color map for each region
region_colors = {
    'north': '#636EFA',
    'east': '#00CC96',
    'south': '#EF553B',
    'west': '#AB63FA'
}

# Initial plot (without any region filter applied)
fig = px.line(df, x="Date", y="Sales", color="Region", line_group="Region", color_discrete_map=region_colors)

# Layout for the app
pink_dash.layout = html.Div(children=[
    html.Div([
        # Header Section
        html.H1('Pink Morsels Sales (February 2018 - February 2022)', className='header-title'),
        html.Div([
            html.P(
                'Price increased from $3.00 to $5.00 on 15th January, 2021. Use the filter below to explore sales data by region.',
                className='intro-text')
        ], className='intro-container'),

        # Region Filter Section
        html.Div([
            html.Label('Filter by Region:', className='filter-label'),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'},
                    {'label': 'All Regions', 'value': 'all'},
                ],
                value='all',  # Default value
                className='region-radio'
            ),
        ], className='filter-container'),

        # Graph Container
        html.Div([
            dcc.Graph(
                id='sales-graph',
                figure=fig,
                className='graph-container'
            )
        ])
    ], className='main-container'),
])


# Callback to update the graph based on selected region
@pink_dash.callback(
    Output('sales-graph', 'figure'),
    [Input('region-filter', 'value')]
)
def update_graph(region_value):
    if region_value == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['Region'] == region_value]

    # Create a new figure with the filtered data and the consistent color map
    filtered_fig = px.line(filtered_df, x="Date", y="Sales", color="Region", line_group="Region",
                           color_discrete_map=region_colors)
    return filtered_fig

if __name__ == '__main__':
    pink_dash.run(debug=True)