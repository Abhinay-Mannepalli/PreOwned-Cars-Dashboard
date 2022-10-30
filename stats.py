from dash import html
from dash import dcc
from app import app
from navbar import Navbar

import dash_bootstrap_components as dbc
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from dash import Input, Output, State

df = pd.read_csv("data//vehicles_cleaned.csv")
df_duplicate = df.copy(deep=True)
df_duplicate.sort_values(by=["year"], inplace = True)

body = html.Div(
    className="container scalable",
    children=[
        html.Br(),
        html.H1('Statistics and Interesting Findings'),
        html.Br(),
        html.H3('Car Manufacturer Statistics and Findings'),
        dcc.Graph(
           figure  =  px.histogram(df_duplicate[df_duplicate["year"]>=1980],x = "manufacturer",color="manufacturer",animation_frame="year",range_y=[0,1000])
        ),
        # html.Img(src=app.get_asset_url("CarManufacturer_countplot.png")),
        html.Figcaption('Fig 1. Year wise animated histogram of Cars by manufacturers across the US from 1980 to 2022', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li(' Over the years Ford, Cheverolet and Toyota emerge to be the leaders in terms of number of cars manufactured in the US'),
            ]
        ),
        dcc.Graph(
            figure = px.scatter(df, x = 'manufacturer', y = 'AVG_PRICE_BY_MANUFACTURER', color = 'manufacturer')
        ),
        # html.Img(src=app.get_asset_url("average_car_price_by_manufacturer.png")),
        html.Figcaption('Fig 2. Average Car Prices for all manufacturers throughout the US', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Aston Martin, Kia and Tesla have the highest average car price by manufacturer'),
            ]
        ),
        html.Br(),
        html.H3('Statistics and Findings based on Car Fuel'),
        dcc.Graph(
            figure = px.pie(df, values = 'id', names='fuel')
        ),
        # html.Img(src=app.get_asset_url("Fuel_pie_chart.png")),
        html.Figcaption('Fig 3. Pie Chart depicting the type of Fuel used by cars across the US', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Gas run cars are the most manufactured cars, followed by diesel and hybrid'),
                html.Li('The reason gas run cars are so popular is its low average prices as depicted in the plot below'),
            ]
        ),
        html.Br(),
        # dcc.Graph(
        #     figure = px.box(df, x="fuel", y="price")
        # ),
        html.Img(src=app.get_asset_url("price_boxplot_on_fuel.png")),
        html.Figcaption('Fig 4. Boxplot depicting the prices of car based on their fuel types', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Another important inference can take from this plot is that diesel and electric run cars are the most expensive ones by average'),
                html.Li('It seems appropriate for electric cars to be expensive due to them the new and upcoming technology in the market'),
                html.Li('The reason diesel cars come up in top 3 when it comes to highest average prices can be inferred from the two plots below'),
            ]
        ),
        html.Img(src=app.get_asset_url("fuel_historgam_car_type.png")),
        html.Figcaption('Fig 5. Histogram depicting count of different car types based on their fuel', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Truck and pickup cars are the top 2 car types which come up in diesel usage'),
                html.Li('The plot below depicts how when it comes to prices, truck and pickup cars peak on the charts'),
            ]
        ),
        html.Br(),
        html.Img(src=app.get_asset_url("price_boxplot_on_car_type.png")),
        html.Figcaption('Fig 6. Boxplot depicting car prices based on their types', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Trucks and pickups have a higher average than all the type of cars available(excluding the outliers) which explains as to why diesel cars have a higher average than the other type of cars'),
            ]
        ),
        html.Br(),
        dcc.Graph(
            figure = px.histogram(df[df['year']>=1980], x = 'year', color = 'year')
        ),
        # html.Img(src=app.get_asset_url("car_sales_over_the_years.png")),
        html.Figcaption('Fig 9. Histogram of State wise Cars sold across the US from 1980 to 2021', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('From the year 1980, the number of car sales per year have increased from 1980 steadily till 2008'),
                html.Li('There is a break from trend in the year 2009 and again in 2021'),
            ]
        ),
        dcc.Graph(
            figure = px.scatter(df[df['year']>=1980], x = 'year', y = 'AVG_PRICE_BY_YEAR')
        ),
        # html.Img(src=app.get_asset_url("average_price_over_the_years.png")),
        html.Figcaption('Fig 10. Scatterplot depicting avg car prices sold across all states based on years 1980 tp 2021', style = {'text-align':'center', 'font-size':'13px', 'color':'gray'}),
        html.Br(),
        html.Ul(
            children=[
                html.Li('Travering from the left,we can see a sharp fall in prices of average prices from early 1990s to 2000 , which can be attributed to:'),
                html.Ol(
                    children=[
                        html.Li(
                            html.A(
                                'The sharp increase in oil prices during 1990 which may have encouraged people to buy cars with high mileage(normal cars) instead of low mileage cars(sports cars usually, luxury even)', 
                                href='https://www.cnbc.com/2020/01/03/spiking-oil-prices-have-led-to-recessions-in-the-past-and-thats-why-the-stock-market-is-on-edge.html#:~:text=The%20last%20three%20U.S.%20recessions,crude%20shot%20up%20nearly%20135%25.', 
                                target="_blank"
                            )
                        ),
                        html.Li(
                            html.A(
                                'The financial crash due to dot com bubble burst from 1995 to 2000', 
                                href='https://www.investopedia.com/terms/d/dotcom-bubble.asp#:~:text=Equities%20entered%20a%20bear%20market,Internet%20companies%20to%20go%20bust', 
                                target="_blank"
                            )
                        ),
                    ]
                ),
                html.Li('We then see a trend of increase in average car prices from 2000 to 2008, with a sudden drop in 2009, which can be attributed to the economic crisis of 2008-09, followed by another trend of increase in car prices(average) till 2020'),
                html.Li('The drop in car prices from 2020 to 2021, can be attributed to the COVID-19 pandemic.With people social distancing, which means less requirement of travel and with increasing work from home culture, brought a sudden drop of car sales, which might have brought upon this sudden drop in average prices'),
            ]
        ),
    ]
)

nav = Navbar()
def Stats(): 
    layout = html.Div([
        nav,
        body
    ])
    return layout

app.layout = Stats()

if __name__ == "__main__":
    app.run_server(debug=True)
