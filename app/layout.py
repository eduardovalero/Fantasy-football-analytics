import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
from config import (chart_info, chart_titles, page_info, page_titles,  page_suptitles)


# -------------------------------- Header -------------------------------------
header = dbc.Col(
    dbc.Navbar(
        className='my-navbar',
        children=[
            html.Img(
                className='ms-4',
                src='assets/favicon.svg',
                height='80rem'),
            dbc.NavbarBrand(
                className='ms-4',
                children='Biwenger analytics',
                style={'font-weight': '600'}),
            dbc.Button(
                className='ms-2',
                id='home-btn',
                n_clicks=0,
                children='Market',
                href='/',
                outline=True,
                color='light'),
            dbc.Button(
                className='ms-2',
                id='players-btn',
                n_clicks=0,
                children='Players',
                href='/players',
                outline=True,
                color='light')
        ],
        color='#1C3146',
        dark=True
    ),
    style={"padding": "0"}
)

# ------------------------------- Sidebar -------------------------------------

# Sidebar object
sidebar = dbc.Col(
    id='sidebar',
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
                    id='budget-accordion',
                    title=chart_titles['budget'],
                    children=[
                        html.P(chart_info['budget']),
                        dbc.Input(id="input-budget", type="number", min=0, max=100, step=1, placeholder="20"),
                        dbc.Button('Calculate', className='btn-accordion mt-2', id='btn-budget', n_clicks=0),
                        ]),
                dbc.AccordionItem(
                    id='payments-accordion',
                    title=chart_titles['payments'],
                    children=[
                        html.P(chart_info['payments']),
                        dbc.Button('Display', className='btn-accordion', id='btn-payments', n_clicks=0)]),
                dbc.AccordionItem(
                    id='links-accordion',
                    title=chart_titles['links'],
                    children=[
                        html.P(chart_info['links']),
                        dbc.Button('Display', className='btn-accordion', id='btn-links', n_clicks=0)]),
                dbc.AccordionItem(
                    id='signings-accordion',
                    title=chart_titles['signings'],
                    children=[
                        html.P(chart_info['signings']),
                        dbc.Button('Display', className='btn-accordion', id='btn-signings', n_clicks=0)])
            ]
        ),
        dbc.Accordion(
            id='player-accordion',
            start_collapsed=True,
            children=[
                dbc.AccordionItem(
                    id='performance-accordion',
                    title=chart_titles['performance'],
                    children=[
                        html.P(chart_info['performance']),
                        dbc.Button('Display', className='btn-accordion', id='btn-performance', n_clicks=0)
                    ]
                )
            ]
        )
    ]
)

# -------------------------------- Chart --------------------------------------
chart = dbc.Col(
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
        dbc.Row(children=header),
        dbc.Row(children=[sidebar, chart]),
        dcc.Store(id='market-data'),
        dcc.Store(id='players-data')
    ],
    fluid=True
)
