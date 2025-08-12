import csv

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

pink_dash = Dash()

sales = []
date = []
region = []

with open('data/pink_morsels_data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sales.append(float(row['sales']))
        date.append(row['date'])
        region.append(row['region'])

df = pd.DataFrame({
    "Sales": sales,
    "Date": pd.to_datetime(date),
    "Region": region
})

fig = px.line(df, x="Date", y="Sales", color="Region", line_group="Region")

pink_dash.layout = html.Div(children=[
    html.H1(children='Pink Morsels Sales (February 2018 - February 2022)'),

    html.Div(children='''
    Price increased from $3.00 to $5.00 on 15th January, 2021.
'''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    pink_dash.run(debug=True)