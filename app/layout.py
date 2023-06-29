import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
from config import (chart_info, chart_titles, page_info, page_titles,  page_suptitles)


# -------------------------------- App header -------------------------------------
header = dbc.Row(
    dbc.Navbar(
        id='navbar',
        children=[
                html.Img(
                    src='assets/favicon.svg',
                    width='75vh',
                    style={'margin-left': '3rem'}
                ),
                dbc.NavbarBrand(
                    children='Biwenger analytics',
                    style={'font-weight': '600'}
                ),
                dbc.Button(
                    id='market-btn',
                    n_clicks=0,
                    children='Market',
                    href='/',
                    outline=True,
                    color='light'
                ),
                dbc.Button(
                    id='players-btn',
                    n_clicks=0,
                    children='Players',
                    href='/players',
                    outline=True,
                    color='light'
                )
        ],
        color='#1C3146',
        dark=True,
        style={'margin': '0rem !important'}
    ),
)

# --------------------------- App body  ---------------------------------
core = dbc.Row(
    id='core',
    style={'height': '100vh', 'margin-right': '0rem'},
    children=[
        dbc.Col(
            id='sidebar',
            width=3,
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
                html.Hr(
                ),
                html.P(
                    id='sidebar-info',
                    children=page_info['market'],
                    className='lead',
                    style={'font-size': '1.25rem', 'font-weight': '400', 'text-align': 'justify'}),
                dbc.Accordion(
                    id='market-accordion',
                    start_collapsed=True,
                    children=[
                        dbc.AccordionItem(
                            id='budget-accordion',
                            title=chart_titles['budget'],
                            children=[
                                html.P(chart_info['budget']),
                                dcc.Slider(0, 100, 1, id='budget-slider', value=20, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                                dbc.Button('Calculate', className='btn-accordion mt-2', id='btn-budget', n_clicks=0),
                            ]
                        ),
                        dbc.AccordionItem(
                            id='links-accordion',
                            title=chart_titles['links'],
                            children=[
                                html.P(chart_info['links']),
                                dbc.Button('Display', className='btn-accordion mt-2', id='btn-links', n_clicks=0),
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
                                dbc.Button('Display', className='btn-accordion', id='btn-efficiency', n_clicks=0)
                            ]
                        ),
                        # dbc.AccordionItem(
                        #     id='fitness-accordion',
                        #     title=chart_titles['fitness'],
                        #     children=[
                        #         html.P(chart_info['fitness']),
                        #         dbc.Button('Display', className='btn-accordion', id='btn-fitness', n_clicks=0)
                        #     ]
                        # )
                    ]
                )
            ],
        ),
        dbc.Col(
            id='chart',
            width=6,
            children=[dbc.Spinner(
                children=[
                    html.Div(
                        children=[dcc.Graph(id='chart-content', figure={})],
                        style={'display': 'none'},
                        id='chart-container'
                    )],
                fullscreen=True,
                color='primary',
                spinner_style={'width': '10rem', 'height': '10rem'},
                fullscreen_style={'opacity': '0.5'}
            )]
        ),
        dbc.Col(
            id='twitter-feed',
            width=3,
            children=[
                html.Div(
                    html.Iframe(
                        id='twitter-widget',
                        srcDoc='''
                            <a class="twitter-timeline" data-theme="light" href="https://twitter.com/biwenger?ref_src=twsrc%5Etfw"></a> 
                            <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
                        ''',
                        style={'width': '100%', 'height': '100%', 'margin': '0rem', 'overflow': 'hidden'},
                    ),
                    style={'height': '100%', 'margin': '1rem'}
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
                    children=["Sign in to Biwenger"]
                ),
                close_button=False
            ),
            dbc.ModalBody(
                id='modal-body',
                children=[
                    html.P(
                        id='modal-text',
                        children='Input your details and then click Sign in to access the app and start analyzing you league.',
                        style={'color': 'primary', 'margin-bottom': '2rem'}
                    ),
                    dbc.InputGroup([
                            dbc.InputGroupText('Email'),
                            dbc.Input(id='modal-email', placeholder='john.doe@gmail.com')],
                        className='mb-3',
                    ),
                    dbc.InputGroup([
                            dbc.InputGroupText('Password'),
                            dbc.Input(id='modal-password', type='password', placeholder='u!4FyW*xj27$')],
                        className='mb-3',
                    ),
                    dbc.InputGroup([
                            dbc.InputGroupText('User ID'),
                            dbc.Input(id='modal-user', placeholder='7820380')],
                        className='mb-3',
                    ),
                    dbc.InputGroup([
                            dbc.InputGroupText('League ID'),
                            dbc.Input(id='modal-league', placeholder='512626')],
                        className='mb-3',
                    )
                ],
            ),
            dbc.ModalFooter([
                dbc.Button(
                    id="modal-btn",
                    children=["Sign in"],
                    className="ms-auto",
                    n_clicks=0,
                )
            ]),
        ],
    )

# ------------------------------- Layout --------------------------------------
layout = dbc.Container(
    children=[
        dcc.Location(id='url'),
        modal,
        header,
        core,
        dbc.Spinner(
            children=[dcc.Store(id='app-data')],
            fullscreen=True,
            color='primary',
            spinner_style={'width': '10rem', 'height': '10rem'},
            fullscreen_style={'opacity': '0.5', 'position': 'fixed', 'z-index': '999999'}
        )
    ],
    fluid=True,
    style={'padding': '0rem', 'margin': '0rem'}
)
