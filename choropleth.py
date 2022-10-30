import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from numpy.core.shape_base import stack
import plotly.express as px
import pandas as pd 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
from navbar import Navbar

nav = Navbar()
car_year=[2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980]
manufacturer=['gmc', 'chevrolet', 'toyota', 'ford', 'jeep', 'nissan', 'ram','mazda', 'cadillac', 'honda', 'dodge', 'lexus', 'jaguar', 'buick','chrysler', 'volvo', 'audi', 'infiniti', 'lincoln', 'alfa-romeo','subaru', 'acura', 'hyundai', 'mercedes-benz', 'bmw', 'mitsubishi','volkswagen', 'porsche', 'kia', 'ferrari', 'mini', 'pontiac','fiat', 'rover', 'tesla', 'saturn', 'mercury', 'harley-davidson','datsun', 'aston-martin', 'land rover']

df = pd.read_csv("data//vehicles_cleaned.csv")
df = df.drop(["Unnamed: 0"], axis = 1)

body = html.Div(
    className="container scalable",
    children=[
        html.Br(),
        html.P(
            children="Choose car listings on the map",
        ),
        html.Br(),
        html.Div(
            className="control-row-1",
            children=[
                html.Div(
                    id="state-select-outer",
                    children=[
                        html.Label("Select States"),
                        dcc.Dropdown(
                            id="state-select",
                            options=[{"label": i, "value": i} for i in df['state'].unique()],
                            value=['nj','ny'], 
                            multi=True,
                        ),
                    ],
                ),
                html.Div(
                    id="select-metric-outer",
                    children=[
                        html.Label("Choose the year of Vehicle"),
                        dcc.Dropdown(
                            id="car-year-select",
                            options=[{"label": i, "value": i} for i in car_year],
                            value=[car_year[0], car_year[1], car_year[2]],
                            multi=True,
                        ),
                    ],
                ),
            ],
        ),
        html.Br(),
        html.Div([
            html.Label("Drag the Slider to Change the Price"),
            dcc.RangeSlider(
                id='price-select',
                min=0,
                max=50000,        
                value=[5000, 30000],
                marks={
                    0: {'label': '0'},
                    5000: {'label': '5000'},
                    10000: {'label': '10000'},
                    15000: {'label': '15000'},
                    20000: {'label': '20000'},
                    25000: {'label': '25000'},
                    30000: {'label': '30000'},
                    35000: {'label': '35000'},
                    40000: {'label': '40000'},   
                    45000: {'label': '45000'},                     
                    50000: {'label': '50000'}
                }
            ),
            html.Div(id='output-container-price-slider')
        ]),
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
                            children="Car listings in the selected states",
                        ),
                        html.Div(
                            id="geo-map-loading-outer",
                            children=[
                                dcc.Loading(
                                    id="loading",
                                    children=dcc.Graph(
                                        id="geo-map",
                                        figure={
                                            "data": [],
                                            "layout": go.Layout(paper_bgcolor='rgb(255, 250, 205)')
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

def Choropleth(): 
    layout = html.Div([
        nav,
        body
    ])
    return layout

@app.callback(
    Output("geo-map", "figure"), 
    [
        Input("state-select", "value"),
        Input("car-year-select", "value"),
        Input("price-select", "value"),  
    ],
)
def update_map(state_select, car_year_select, price_select):
    dff = df[
        df["state"].isin(state_select) & df["year"].isin(car_year_select) & (df["price"] >= price_select[0]) & (df["price"] <= price_select[1])
    ]
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
                # bgcolor = "rgb(255, 250, 205)",
                landcolor = "rgb(255, 250, 205)",
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

app.layout = Choropleth()

if __name__ == "__main__":
    app.run_server(debug=True)