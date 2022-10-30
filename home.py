from dash import html
from dash import dcc
from app import app
from navbar import Navbar

nav = Navbar()

body = html.Div(
    className="container scalable",
    children=[
        html.Br(),
        html.Div([
            html.H1(children='The one stop-shop for car requirements', style = {'text-align':'center', 'color': '#772953'})
        ]),
        html.Br(),
        html.Div(
            [
                dcc.Markdown(
                    """
                        # **About The Application**
                        The PreOwnedCars Dashboard is an interactive web application consisting of more than 400K records of used cars across the United States of America.
                        The data used is obtained from Kaggle (originally scraped from craigslist.com).
                        This application has been created as a part of final project for the Course CS526: Data Interaction and Visual Analytics.
                        This web application explores the dataset in depth, providing insight on trends of different variables over the years and other more useful information. 
                        This dashboard was created to create a one stop shop for helping users select the optimal car, the one which meets the user's monetary and technical requirements.

                        # **Data**
                        The data-set is from Kaggle and is the world's largest collection of used vehicles for sale from Craigslist. 
                        The data is scraped every few months, it contains all the relevant information on car sales including columns namely:
                        - Price
                        - Year
                        - State
                        - Latitude
                        - Longitude
                        - Odometer
                        - Manufacturer
                        - Model
                        - Condition
                        - Fuel

                        The data consists of around of 400K rows and 22 columns, measuring upto 1.46GB in computer memory. 

                        The data is static by nature and time variance is essential.

                        # **Fundamental Questions**
                        **Q1) What features make the app interactive?** 

                        We have added the following technicalities to make our app interactive:

                        - Interface Layout - Overview of the entire Data Set (Choropleth maps), Nationwide data visualization for all the selected features yearwise.
                        - Interface interaction mechanisms and answers representation for further user interaction - Both textual and graphical
                        - Mouse Clicks, Mouse Hovering, Mouse Selection and their combinations - Mouse Clicks, Mouse Hovering
                        - Basic visual data elements controls : size, color, texture
                        - Panning
                        - Zooming: Mouse control, Elastic Window
                        - Linking of different views - Nationwide to state wise data visualization
                        - Search Functionality - Users can run queries to generate custom choropleth maps

                        **Q2) How does the application influence user's selection of car?** 

                        We have made use of different plots, each exploiting different features that concerns the user. Some of the plots are:
                        - Bar plot displaying average price of cars by region
                        - Violin plot that depicts statewise prices of cars by different manufacturers.
                        - Histograms depcting yearwise sales of total number of cars
                        - A bar graph showcasing average prices of cars by different manufacturers
                        - Box plots creating a display of average prices of car per state.

                        ## **Target Audience**
                        The app mainly targets the following categories of users:
                        - The Buyers & Sellers of used cars
                        - Car manufacturing corporations.
                        - Statisticians and researchers
                    """
                , style={'font-size': '20px'})
            ],
            className="home",
        )
    ]
)

def Homepage(): 
    layout = html.Div([
        nav,
        body
    ])
    return layout

app.layout = Homepage()

if __name__ == "__main__":
    app.run_server(debug=True)
