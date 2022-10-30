from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from app import app
from home import Homepage
from stats import Stats
from plots import Plots
from choropleth import Choropleth
from choropleth_adv import Choropleth_adv

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/stats':
        return Stats()
    elif pathname == '/plots':
        return Plots()
    elif pathname == '/choropleth':
        return Choropleth()
    elif pathname == '/choropleth_adv':
        return Choropleth_adv()
    else:
        return Homepage()

if __name__ == '__main__':
    app.run_server(debug=False)