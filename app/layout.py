import dash.dcc as dcc
import dash.html as html
from dash import dash_table
import dash_bootstrap_components as dbc
from config import (chart_info, chart_titles, page_info, page_titles,
                    page_suptitles, spinner_dict, slider_dict,
                    style_data, style_header, positions)


# -------------------------- App header ---------------------------------
header = dbc.Row(
    dbc.Navbar(
        id='navbar',
        dark=True,
        children=[
            html.Img(
                id='navbar-img',
                src='assets/favicon.svg'
            ),
            dbc.NavbarBrand(
                id='navbar-brand',
                children='Football Fantasy analytics'
            ),
            dbc.Button(
                id='market-btn',
                n_clicks=0,
                href='/',
                children='Market'
            ),
            dbc.Button(
                id='players-btn',
                n_clicks=0,
                href='/players',
                children='Players'
            )
        ]
    )
)


# --------------------------- App main content  ---------------------------------
core = dbc.Row(
    id='main-content',
    children=[
        dbc.Col(
            id='sidebar',
            width=3,
            children=[
                html.H5(
                    id='sidebar-suptitle',
                    children=page_suptitles['market']
                ),
                html.H3(
                    id='sidebar-title',
                    className='display-4',
                    children=page_titles['market']
                ),
                html.Hr(
                ),
                html.P(
                    id='sidebar-info',
                    className='lead',
                    children=page_info['market']
                ),
                dbc.Accordion(
                    id='market-accordion',
                    start_collapsed=True,
                    children=[
                        dbc.AccordionItem(
                            id='links-accordion',
                            title=chart_titles['links'],
                            children=[
                                html.P(chart_info['links']),
                                dbc.Button('Display', id='btn-links', n_clicks=0),
                            ]
                        )
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
                                dbc.Button('Display', id='btn-efficiency', n_clicks=0)
                            ]
                        ),
                        dbc.AccordionItem(
                            id='fitness-accordion',
                            title=chart_titles['fitness'],
                            children=[
                                html.P(chart_info['fitness']),
                                dbc.Button('Display', id='btn-fitness', n_clicks=0)
                            ]
                        ),
                        dbc.AccordionItem(
                            id='lastseason-accordion',
                            title=chart_titles['lastseason'],
                            children=[
                                html.P(chart_info['lastseason']),
                                dbc.Button('Display', id='btn-lastseason', n_clicks=0)
                            ]
                        ),
                        dbc.AccordionItem(
                            id='advanced-accordion',
                            title=chart_titles['advanced'],
                            children=[
                                html.P(chart_info['advanced']),
                                dbc.Button('Display', id='btn-advanced', n_clicks=0)
                            ]
                        )
                    ]
                )
            ],
        ),
        dbc.Col(
            id='core',
            width=6,
            children=[
                html.Div(
                    id = 'chart-filter',
                    children = [
                        html.Datalist(
                            id='chart-filter-list',
                            children=[]
                        ),
                        html.P(
                            children='Players position',
                            className='filter-title'
                        ),
                        dcc.RadioItems(
                            options=positions,
                            value=False,
                            id='chart-filter-radio',
                            inline=True
                        ),
                        dbc.InputGroup(
                            className='mb-3',
                            children=[
                                dbc.InputGroupText(children='Player 1'),
                                dcc.Input(
                                    id='chart-filter-input1',
                                    placeholder=" Select first player",
                                    type='text',
                                    list='chart-filter-list'
                                ),
                            ]
                        ),
                        dbc.InputGroup(
                            className='mb-3',
                            children=[
                                dbc.InputGroupText('Player 2'),
                                dcc.Input(
                                    id='chart-filter-input2',
                                    placeholder=" Select second player",
                                    type='text',
                                    list='chart-filter-list')
                            ]
                        ),
                        dbc.Button(
                            id='btn-chart-filter',
                            n_clicks=0,
                            disabled=True,
                            children='Compare'
                        ),
                    ]
                ),
                dbc.Spinner(
                    **spinner_dict,
                    children=[
                        html.Div(
                            id='chart-container',
                            children=[dcc.Graph(id='chart-content')]
                        )
                    ],
                )
            ]
        ),
        dbc.Col(
            id='information',
            width=3,
            children=[
                html.Div(
                    id='scoreboard-container',
                    children=[
                        html.H5(id='scoreboard-title', children='League scoreboard'),
                        dash_table.DataTable(
                            id='scoreboard-content',
                            sort_action='native',
                            style_header=style_header,
                            style_data=style_data
                        ),
                        html.P(className='filter-title', children='Initial budget (M)'),
                        dcc.Slider(0, 100, 1, id='scoreboard-slider', value=20, **slider_dict),
                    ]
                ),
                html.Div(
                    id = 'table-container',
                    children=[
                        html.H5(
                            id='table-title',
                            children='Top performances from last season'
                        ),
                        dash_table.DataTable(
                            id='table-content',
                            sort_action='native',
                            style_header=style_header,
                            style_data=style_data
                        ),
                        html.Div(
                            id='table-filter',
                            children=[
                                dbc.Col(
                                    id='table-filter-position',
                                    width=6,
                                    children=[
                                        html.P('Position', className='filter-title'),
                                        dcc.RadioItems(positions, 'forward', id='lastseason-radio', inline=False)
                                    ]
                                ),
                                dbc.Col(
                                    id='table-filter-price',
                                    width=6,
                                    children=[
                                        html.P('Price range (millions)', className='filter-title'),
                                        dcc.RangeSlider(id='lastseason-slider', min=0, max=30, value=[5, 25], **slider_dict)
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


# ---------------------------- App modal ------------------------------------
modal = dbc.Modal(
    id="modal",
    centered=True,
    is_open=True,
    backdrop='static',
    keyboard=False,
    children=[
            dbc.ModalHeader(
                dbc.ModalTitle(
                    id='modal-title',
                    children=["Sign in to your Football Fantasy app"]
                ),
                close_button=False
            ),
            dbc.ModalBody(
                id='modal-body',
                children=[
                    html.P(
                        id='modal-text',
                        children='Input your details to start analyzing you league.'
                    ),
                    dbc.InputGroup(
                        className='mb-3',
                        children=[
                            dbc.InputGroupText('Email'),
                            dbc.Input(id='modal-email', placeholder='john.doe@gmail.com', type='text')
                        ]
                    ),
                    dbc.InputGroup(
                        className='mb-3',
                        children=[
                            dbc.InputGroupText('Password'),
                            dbc.Input(id='modal-password', type='password', placeholder='u!4FyW*xj27$')
                        ]
                    ),
                    dbc.InputGroup(
                        className='mb-3',
                        children=[
                            dbc.InputGroupText('User ID'),
                            dbc.Input(id='modal-user', placeholder='7820380', type='text')
                        ]
                    ),
                    dbc.InputGroup(
                        className='mb-3',
                        children=[
                            dbc.InputGroupText('League ID'),
                            dbc.Input(id='modal-league', placeholder='512626', type='text')
                        ]
                    )
                ],
            ),
            dbc.ModalFooter(
                children=[
                    dbc.Button(
                        id="modal-btn",
                        className="ms-auto",
                        n_clicks=0,
                        children=["Sign in"]
                    )
                ]
            ),
        ],
    )


# ------------------------------- Layout --------------------------------------
layout = html.Div(
    id='layout',
    children=[
        dcc.Location(id='url'),
        modal,
        header,
        core,
        dbc.Spinner(children=[dcc.Store(id='app-data')], **spinner_dict)
    ]
)
