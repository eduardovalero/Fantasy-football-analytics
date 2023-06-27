import io
import json
import base64
import pandas as pd
from pandas import json_normalize
from layout import layout
import dash_bootstrap_components as dbc
from time import strftime, strptime, localtime, mktime
from config import page_info, page_titles, page_suptitles
from dash import Dash, dcc, no_update, Input, Output, State, callback_context
import functions as api

# ------------------------ Initialization ----------------------------

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = layout

# ------------------------ Login callback ----------------------------
@app.callback(
    Output('market-data', 'data'),
    Output('rounds-data', 'data'),
    Output('players-data', 'data'),
    Output('modal-text', 'children'),
    Output("modal", "is_open"),
    Input('modal-btn', 'n_clicks'),
    State('modal-email', 'value'),
    State('modal-password', 'value'),
    State('modal-user', 'value'),
    State('modal-league', 'value'),
    prevent_initial_call=True
)
def login(button, email, password, user, league):
    try:
        session, token = api.login(email, password)
        # Request market data
        epoch = int(mktime(strptime('23-06-2022 05:00:00', '%d-%m-%Y %H:%M:%S')))
        market_df, rounds_df = api.get_market(session, token, epoch, league, user)
        market_json = market_df.to_json()
        # Remove duplicates from rounds_df (this happens when a player performance is corrected)
        rounds_df.drop_duplicates(subset=['round', 'member'], inplace=True)
        rounds_json = rounds_df.to_json()
        # Request players data
        players_df = api.get_players(session)
        players_json = players_df.to_json()
        # Return on success
        return market_json, rounds_json, players_json, no_update, False
    except:
        # Return on exception
        return no_update, no_update, no_update, 'Error during loging. Try again.', no_update


# ------------------------ Routes callback ----------------------------
@app.callback(
    Output("sidebar-suptitle", "children"),
    Output("sidebar-title", "children"),
    Output("sidebar-info", "children"),
    Output("market-accordion", "style"),
    Output("player-accordion", "style"),
    Input("url", "pathname")
)
def update_accordion(path):
    if path == "/":
        return page_suptitles['market'], page_titles['market'], page_info["market"], {"display": "block"}, {"display": "none"}
    elif path == "/players":
        return page_suptitles['players'], page_titles['players'], page_info["players"], {"display": "none"}, {"display": "block"}
    else:
        pass


# ------------------------ Chart callback ----------------------------
@app.callback(
    Output('chart', 'children'),
    Input('btn-budget', 'n_clicks'),
    State('market-data', 'data'),
    State('rounds-data', 'data'),
    State('input-budget', 'value'),
    prevent_initial_call=True
)
def update_chart(button, market_data, rounds_data, initial_budget):
    # Get trigger
    trigger = callback_context.triggered[0]['prop_id'].split('.')[0]
    # Check trigger element
    if trigger == 'btn-budget':
        # Update chart
        market_df = pd.DataFrame(json.loads(market_data))
        rounds_df = pd.DataFrame(json.loads(rounds_data))
        fig = api.plot_budgets(initial_budget, market_df, rounds_df)
        return dcc.Graph(figure=fig)
    else:
        return no_update


# ------------------------ Run the app ----------------------------
if __name__ == '__main__':
    app.run_server(
        debug=False,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )