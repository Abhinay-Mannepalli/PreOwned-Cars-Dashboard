import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from numpy.core.shape_base import stack
import plotly.express as px
import pandas as pd 
import plotly.graph_objs as go
import numpy as np
from plotly.subplots import make_subplots
from app import app
from navbar import Navbar

nav = Navbar()
df = pd.read_csv("data//vehicles_cleaned.csv")

body = html.Div(
    className="container scalable",
    children=[
        html.Br(),
        html.H1('Plots'),
        html.Br(),
        dcc.Dropdown(
            placeholder = 'Select State...',
            id='dpdn2', 
            value=['nj','ny'], 
            multi=True, 
            options=[{'label': x, 'value': x} for x in df.state.unique()]
        ),
        # dcc.Dropdown(
        #     placeholder = 'Select region...',
        #     id='dpdn3', 
        #     value=['south jersey','north jersey'], 
        #     multi=True, 
        #     options=[{'label': x, 'value': x} for x in df.region.unique()]
        # ),
        # dcc.Dropdown(
        #     placeholder = 'Select Manufacturer...',
        #     id='dpdn3', 
        #     value=['lexus','mazda'], 
        #     multi=True, 
        #     options=[{'label': x, 'value': x} for x in df.manufacturer.unique()]
        # ),
        html.Br(),
        html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(id='bar-plot', figure={})),
                dbc.Col(dcc.Graph(id='histogram-plot', figure={})),
            ]),
        ]),
        html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(id='violin-plot', figure={})),
                dbc.Col(dcc.Graph(id='line-plot', figure={})),
            ]),
        ]),
        html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(id='piechart-plot', figure={})),
                dbc.Col(dcc.Graph(id='donut-plot', figure={})),
            ]),
        ]),

                html.Br(),
        html.Div([
            dbc.Row([
            dbc.Col(dcc.Dropdown(
            placeholder = 'Select region...',
            id='dpdn3', 
            value=['south jersey','north jersey'], 
            multi=True, 
            options=[{'label': x, 'value': x} for x in df.region.unique()]
        )),     
         dbc.Col(dcc.Dropdown(
            placeholder = 'Select Manufacturer...',
            id='dpdn4', 
            value=['lexus','mazda'], 
            multi=True, 
            options=[{'label': x, 'value': x} for x in df.manufacturer.unique()]
        )),


            ]),
        ]),
                html.Br(),
                html.Div([
            dbc.Row([
                dbc.Col(dcc.Graph(id='sunburst_plot', figure={})),
                dbc.Col(dcc.Graph(id='polar_plot', figure={})),
            ]),
        ]),

    ]
)

def Plots(): 
    layout = html.Div([
        nav,
        body
    ])
    return layout

@app.callback(
    Output(component_id='bar-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
   # Input(component_id='dpdn3', component_property='value'),
    #Input(component_id='dpdn4', component_property='value'),
)
def update_graph(states_chosen):
    dff = df[(df['year']==2000) & df.state.isin(states_chosen)].drop_duplicates(subset = ["manufacturer","AVG_PRICE_BY_MANUFACTURER"])
    fig = px.bar(dff, x="manufacturer",y="AVG_PRICE_BY_MANUFACTURER",color="AVG_PRICE_BY_MANUFACTURER")
    fig.update_layout(
        title={
            'text': ' Manufacturers vs Avg price of Manufacturers cars ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
        )
    return fig

@app.callback(
    Output(component_id='histogram-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(states_chosen):
    dff = df[(df['year']>=1980) & df.state.isin(states_chosen)] 
    fig = px.histogram(dff, x = 'year', color = 'year')
    fig.update_layout(
        title={
            'text': ' Total number of Cars sold vs Year ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

@app.callback(
    Output(component_id='violin-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(states_chosen):
    fig = px.violin(df[df["state"].isin(states_chosen)], x = 'state', y='price', color="state")
    fig.update_layout(
        title={
            'text': ' State vs Price of cars ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(state_chosen):
    dff = df[(df['year']>=1980) & df.state.isin(state_chosen)].drop_duplicates(subset = ["state", "year"]).sort_values(by=['state', 'year'])
    fig = px.line(dff, x='year', y='AVG_PRICE_BY_STATE_AND_YEAR', color='state')
    fig.update_traces(mode='lines+markers') 
    fig.update_layout(
    title={
        'text': " Line Chart showing Increase in yearly prices ",
        'y':0.92,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig

@app.callback(
    Output(component_id='piechart-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(states_chosen):
    dff = df[df['state'].isin(states_chosen)].groupby(['state']).mean()
    dff = dff.rename_axis(None, axis=1).reset_index()
    fig = px.pie(dff, names = 'state', values = 'odometer')
    fig.update_layout(
        title={
            'text': ' Average Odometer Comparison between states ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

@app.callback(
    Output(component_id='donut-plot', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(state_chosen):
    dff = pd.pivot_table(df[(df['year'] >= 1980) & df.state.isin(state_chosen)], index=['state'], columns=['fuel'], values=['type'], aggfunc=len, fill_value=0)
    dff.columns = dff.columns.droplevel()
    dff = dff.rename_axis(None, axis=1).reset_index()
    fig = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'},{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=dff['state'], values = dff['gas'], name="Gas"),1, 1)
    fig.add_trace(go.Pie(labels=dff['state'], values = dff['diesel'], name="Diesel"),1, 2)
    fig.add_trace(go.Pie(labels=dff['state'], values = dff['hybrid'], name="Hybrid"),2, 1)
    fig.add_trace(go.Pie(labels=dff['state'], values = dff['electric'], name="Electric"),2, 2)    

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
    title={
        'text': ' Car fuel type comparison between states ',
        'y':0.92,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Gas', x=0.18, y=0.5, font_size=15, showarrow=False),
                 dict(text='Diesel', x=0.83, y=0.5, font_size=15, showarrow=False),
                 dict(text='Hybrid', x=0.16, y=-0.1, font_size=15, showarrow=False),
                 dict(text='Electric',x=0.84, y=-0.1, font_size=15, showarrow=False)])

    return fig


@app.callback(
    Output(component_id='sunburst_plot', component_property='figure'),
    Input(component_id='dpdn3', component_property='value'),
    Input(component_id='dpdn4', component_property='value'),
)
def update_graph(region_chosen,manufacturer_chosen):
    dff = df[(df['region'].isin(region_chosen) & (df['manufacturer'].isin(manufacturer_chosen)))] 
    fig = px.sunburst(dff, path=['region', 'manufacturer','AVG_PRICE_BY_MANUFACTURER'],hover_name="manufacturer", hover_data=["AVG_PRICE_BY_MANUFACTURER","AVG_PRICE_IN_STATE"],color='manufacturer',maxdepth=2,branchvalues='remainder')
    fig.update_layout(
        title={
            'text': ' Region vs Manufacturer ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

@app.callback(
    Output(component_id='polar_plot', component_property='figure'),
    Input(component_id='dpdn3', component_property='value'),
    Input(component_id='dpdn4', component_property='value'),
)
def update_graph(region_chosen,manufacturer_chosen):
  dff2 = pd.DataFrame(dff).reset_index()    dff = df[(df['region'].isin(region_chosen) & (df['manufacturer'].isin(manufacturer_chosen)))].groupby(['region','manufacturer']).mean()

    fig = px.bar(dff2, x="region", y="price", color="manufacturer", title="Long-Form Input",barmode = 'group') 
    fig.update_layout(
        title={
            'text': ' Region vs Average price of a Manufacturer in region ',
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    return fig

app.layout = Plots()

if __name__ == "__main__":
    app.run_server(debug=True)