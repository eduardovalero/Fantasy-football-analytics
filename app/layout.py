import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
from config import (chart_info, chart_titles, page_info, page_titles,
                       market_guide, player_guide, page_suptitles)


# -------------------------------- Header -------------------------------------
header = dbc.Navbar(
    className='my-header',
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    html.Img(
                        src='assets/favicon.svg',
                        height='80px',
                        style={'marginLeft': '2rem'})),
                dbc.Col(
                    dbc.NavbarBrand(
                        children='Biwenger analytics'),
                        style={'font-weight': '600'}),
                dbc.Col(
                    dbc.Button(
                        id='home-btn',
                        n_clicks=0,
                        children='Market',
                        href='/',
                        outline=True,
                        color='light')),
                dbc.Col(
                    dbc.Button(
                        id='players-btn',
                        n_clicks=0,
                        children='Players',
                        href='/players',
                        outline=True,
                        color='light'))
            ],
            align='center',
        ),

    ],
    color='#1C3146',
    dark=True,
)

# ------------------------------- Sidebar -------------------------------------

# Sidebar object
sidebar = html.Div(
    id='sidebar',
    className='my-sidebar',
    children=[
            html.H5(
                id='sidebar-suptitle',
                children=page_suptitles['market'],
                style={'color': '#2c8cff'}
            ),
            html.H3(
                id='sidebar-title',
                children=page_titles['market'],
                className='display-4',
                style={'font-size': '3rem', 'font-weight': '500'}),
            html.Hr(),
            html.P(
                id='sidebar-info',
                children=page_info['market'],
                className='lead',
                style={'font-size': '1.5rem', 'font-weight': '400', 'text-align': 'justify'}),
            dbc.Accordion(
                id='market-accordion',
                start_collapsed=True,
                children=[
                    dbc.AccordionItem(
                        id='boxplot-accordion',
                        title=chart_titles['boxplot'],
                        children=[
                            html.P(chart_info['boxplot']),
                            dbc.Button('Display', className='btn-accordion', id='btn-boxplot', n_clicks=0)]),
                    dbc.AccordionItem(
                        id='sankey-accordion',
                        title=chart_titles['sankey'],
                        children=[
                            html.P(chart_info['sankey']),
                            dbc.Button('Display', className='btn-accordion', id='btn-sankey', n_clicks=0)]),
                    dbc.AccordionItem(
                        id='scatter-accordion',
                        title=chart_titles['scatter'],
                        children=[
                            html.P(chart_info['scatter']),
                            dbc.Button('Display', className='btn-accordion', id='btn-scatter', n_clicks=0)])]),
            dbc.Accordion(
                id='player-accordion',
                start_collapsed=True,
                children=[
                    dbc.AccordionItem(
                        id='bubble-accordion',
                        title=chart_titles['bubble'],
                        children=[
                            html.P(chart_info['bubble']),
                            dbc.Button('Display', className='btn-accordion', id='btn-bubble', n_clicks=0)
                        ]
                    )
                ]
            )
    ]
)

# -------------------------------- Chart --------------------------------------
chart = html.Div(
        id='my-chart',
        style={'display': 'block'},
                children=[
                    html.Div()
                ]
)


# ------------------------------- Layout --------------------------------------
layout = dbc.Container(
    children=[
        dcc.Location(id='url'),
        header,
        sidebar,
        chart,
        dcc.Store(id='market-data'),
        dcc.Store(id='players-data')
    ],
    fluid=True
)
