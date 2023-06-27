import dash.dcc as dcc
import dash.html as html
import dash_bootstrap_components as dbc
from config import (chart_info, chart_titles, page_info, page_titles,  page_suptitles)


# -------------------------------- App header -------------------------------------
header = dbc.Row(
    dbc.Navbar(
        id='navbar',
        children=[
            dbc.Col(
                html.Img(
                    src='assets/favicon.svg',
                    width='100vh'),
                width=1),
            dbc.Col(
                dbc.NavbarBrand(
                    children='Biwenger analytics',
                    style={'font-weight': '600'}),
                width=1),
            dbc.Col([
                    dbc.Button(
                        id='market-btn',
                        n_clicks=0,
                        children='Market',
                        href='/',
                        outline=True,
                        color='light'),
                    dbc.Button(
                        id='players-btn',
                        n_clicks=0,
                        children='Players',
                        href='/players',
                        outline=True,
                        color='light')],
                width=1),
        ],
        color='#1C3146',
        dark=True,
    ),
)

# --------------------------- App body  ---------------------------------
core = dbc.Row(
    id='core',
    style={'height': '100vh'},
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
                                dcc.Slider(0, 100, 1, id='input-budget', value=20, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
                                dbc.Button('Calculate', className='btn-accordion mt-2', id='btn-budget', n_clicks=0),
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
                                dbc.Button('Display', className='btn-accordion', id='btn-performance', n_clicks=0)
                            ]
                        )
                    ]
                )
            ],
        ),
        dbc.Col(
            id='chart',
            width=6,
            children=[html.Div()]
        ),
        dbc.Col(
            id='login-info',
            width=3,
            children=[
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
            dbc.ModalFooter(
                dbc.Button(
                    id="modal-btn",
                    children=["Sign in"],
                    className="ms-auto",
                    n_clicks=0,
                )
            ),
        ],
    )

# ------------------------------- Layout --------------------------------------
layout = dbc.Container(
    children=[
        dcc.Location(id='url'),
        modal,
        header,
        core,
        dcc.Store(id='market-data'),
        dcc.Store(id='rounds-data'),
        dcc.Store(id='players-data'),
        dcc.Store(id='credentials-data')
    ],
    fluid=True,
    style={'padding': '0px'}
)
