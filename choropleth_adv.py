import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
from numpy.core.shape_base import stack
import plotly.express as px
import pandas as pd 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
from navbar import Navbar
from pandasql import sqldf

nav = Navbar()
pysqldf = lambda q: sqldf(q, globals())

used_cars = pd.read_csv("data//vehicles_cleaned.csv")
used_cars = used_cars.drop(["Unnamed: 0"], axis = 1)

body = html.Div(
    className="container scalable",
    children=[
        html.Br(),
        html.P(
            children="Choose car listings on the map",
        ),
        html.Br(),
        html.Div(
            children=[
                html.Div(
                    id="select-outer",
                    children=[
                        html.Label("Run SQL query"),
                        dcc.Textarea(id='input-textarea', placeholder='Insert SQL query', value='SELECT * from used_cars where manufacturer = "honda" and price > 10000', style={'width': '100%', 'height': 300}),
                        html.Button(id='submit-button', type='submit', children='Submit', className='btn btn-primary')
                    ],
                )
            ],
        ),
        html.Br(),
        html.Div(
            id="upper-container",
            className="row",
            children=[
                html.Div(
                    id="geo-map-outer",
                    children=[
                        html.P(
                            id="map-title",
                            children="Car listings in the US",
                        ),
                        html.Div(
                            id="geo-map-loading-outer",
                            children=[
                                dcc.Loading(
                                    id="loading",
                                    children=dcc.Graph(
                                        id="geo-map-adv",
                                        figure={
                                            "data": [],
                                            "layout": dict(
                                                plot_bgcolor="#171b26",
                                                paper_bgcolor="#171b26",
                                            ),
                                        },
                                    ),
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)

def Choropleth_adv(): 
    layout = html.Div([
        nav,
        body
    ])
    return layout

@app.callback(
    Output("geo-map-adv", "figure"), 
        [Input('submit-button', 'n_clicks')],
        [State('input-textarea', 'value')],
)
def update_map_adv(n_clicks, input_textarea):
    dff = pysqldf(input_textarea)
    dff['text'] = dff['manufacturer'] + ',' + dff['price'].astype(str)+','+dff['paint_color'].astype(str)+','+dff['state'].astype(str)+','+dff['id'].astype(str)
    fig = go.Figure(
        data=go.Scattergeo(
            locationmode = 'USA-states',
            lon = dff['long'],
            lat = dff['lat'],
            text = dff['text'],
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = 'Viridis',
                cmin = dff['price'].min(),
                color = dff['price'],
                cmax = dff['price'].max(),
                # colorbar_title="TESTING"
            )
        )
    )

    fig.update_layout(
            title = 'CAR PRICES',
            geo = dict(
                scope='usa',
                projection_type='albers usa',
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
            margin={"r":0,"t":0,"l":0,"b":0},
        )

    fig.update_geos(
        visible=False, resolution=110, scope="usa",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Blue"
    )
    return fig

app.layout = Choropleth_adv()

if __name__ == "__main__":
    app.run_server(debug=True)
