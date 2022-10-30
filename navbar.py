import dash_bootstrap_components as dbc
from dash import html
from app import app

def Navbar():
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src=app.get_asset_url("logo2.png"), height="70px")),
                            dbc.Col(dbc.NavbarBrand("PreOwned Cars Dashboard", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Stats", href="/stats")),
                        dbc.NavItem(dbc.NavLink("Plots", href="/plots")),
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/choropleth")),
                        dbc.NavItem(dbc.NavLink("Advanced", href="/choropleth_adv")),
                    ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
    )
    return navbar