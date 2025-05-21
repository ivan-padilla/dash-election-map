import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
from dash import Dash, dcc, html, Input, Output
#pio.renderers.default = 'browser'

regionalResults = pd.DataFrame(pd.read_csv('data/regionalResults.csv'))
phRegions = json.load(open('data/regionalMap.json', 'r'))
senators_list = regionalResults.columns[1: ].to_list()

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H4('2025 Midterm Election Analysis'),
    html.P('Senator: '),
    dcc.RadioItems(
    id = 'senator',
    options = senators_list,
    value = senators_list[0],
    inline = True
    ),
    dcc.Graph(id = 'graph'),
])

@app.callback(
    Output('graph', 'figure'),
    Input('senator', 'value'))

def display_choropleth(senator):

    fig = px.choropleth(regionalResults,
                    geojson = phRegions,
                    color = senator,
                    color_continuous_scale = 'Viridis',
                    hover_name = 'region',
                    locations = 'region', 
                    featureidkey = 'properties.name'
                   )
    fig.update_geos(
    showcountries = False,
    showcoastlines = False,
    showland = True,
    fitbounds = 'locations',
    visible = False,
    )

    return fig

if __name__ == "__main__":
    app.run()

server = app.server
