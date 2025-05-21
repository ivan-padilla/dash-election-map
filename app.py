import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
from dash import Dash, dcc, html, Input, Output
#pio.renderers.default = 'browser'

regionalResults = pd.DataFrame(pd.read_csv('data/regionalResults.csv'))
phRegions = json.load(open('data/regionalMap.json', 'r'))
senators_list = regionalResults.columns[2: ].to_list()

app = Dash(__name__)
server = app.server

app.layout = html.Div([

    html.Div([
        html.Div('2025', className = 'title'),
        html.Div('Election Results', className = 'subtitle')],
        className = 'header'),
    
    html.Div([
        dcc.Dropdown(
            id = 'senator',
            options = senators_list,
            value = senators_list[0])], 
        className = 'dropdown'),

    html.Div([
        dcc.Graph(id = 'graph')],
        className = 'graph'),
    
    html.Div([
    html.A(html.Img(src='/assets/linkedin.png'), href='https://www.linkedin.com/in/jov-ivan-padilla/', target='_blank'),
    html.A(html.Img(src='/assets/github.png'), href='https://github.com/ivan-padilla', target='_blank')], 
    className='social-icons')

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
