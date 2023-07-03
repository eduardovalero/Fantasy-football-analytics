import io
import json
import base64
import pandas as pd
from pandas import json_normalize
from layout import layout
import dash_bootstrap_components as dbc
from time import strftime, strptime, localtime, mktime
from config import page_info, page_titles, page_suptitles, epoch
from dash import Dash, dcc, no_update, Input, Output, State, ctx, dash_table
import functions as api

# ------------------------ Initialization ----------------------------

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = layout

# ------------------------ Login callback ----------------------------
@app.callback(
    Output('app-data', 'data'),
    Output('modal-text', 'children'),
    Output('modal', 'is_open'),
    Input('modal-btn', 'n_clicks'),
    State('modal-email', 'value'),
    State('modal-password', 'value'),
    State('modal-user', 'value'),
    State('modal-league', 'value'),
    prevent_initial_call=True
)
def login(button, email, password, user, league):
    if button:
        try:
            # session, token = api.login(email, password)
            # # Request market data
            # market_df, rounds_df = api.get_market(session, token, epoch, league, user)
            # market_json = market_df.to_json()
            # # Remove duplicates from rounds_df (this happens when a player performance is corrected)
            # rounds_df.drop_duplicates(subset=['round', 'member'], inplace=True)
            # rounds_json = rounds_df.to_json()
            # # Request players data
            # players_df = api.get_players(session)
            # players_json = players_df.to_json()
            # # Form app data dict
            # app_data = {'market': market_json, 'rounds': rounds_json, 'players': players_json, 'email': email}
            # Return on success
            # *****************
            app_data ={
                'market': pd.read_excel('../data/market.xlsx').to_json(),
                'rounds': pd.read_excel('../data/rounds.xlsx').to_json(),
                'players': pd.read_excel('../data/players.xlsx').to_json(),
                'email': 'edpvalero@gmail.com'
            }
            # *****************
            return app_data, no_update, False
        except:
            # Return on exception
            return no_update, 'Error during loging. Try again.', no_update
    else:
        return no_update, no_update, no_update


# ------------------------ Routes callback ----------------------------
@app.callback(
    Output('sidebar-suptitle', 'children'),
    Output('sidebar-title', 'children'),
    Output('sidebar-info', 'children'),
    Output('market-accordion', 'style'),
    Output('player-accordion', 'style'),
    Input('url', 'pathname')
)
def update_accordion(path):
    if path == '/':
        return page_suptitles['market'], page_titles['market'], page_info['market'], {'display': 'block'}, {'display': 'none'}
    elif path == '/players':
        return page_suptitles['players'], page_titles['players'], page_info['players'], {'display': 'none'}, {'display': 'block'}
    else:
        pass


# ------------------------ Chart callback ----------------------------
@app.callback(
    Output('chart-content', 'figure'),
    Output('chart-container', 'style'),
    Input('btn-efficiency', 'n_clicks'),
    Input('btn-links', 'n_clicks'),
    Input('btn-fitness', 'n_clicks'),
    State('app-data', 'data'),
    prevent_initial_call=True
)
def update_chart(btn_efficiency, btn_links, btn_fitness, app_data):
    # Get data from session
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    market_df = pd.DataFrame(json.loads(app_data['market']))
    players_df = pd.DataFrame(json.loads(app_data['players']))
    # Deliver desired info
    if trigger == 'btn-efficiency':
        return api.plot_player_efficiency(players_df), {'display': 'block'}
    elif trigger == 'btn-links':
        return api.plot_links(market_df), {'display': 'block'}
    elif trigger == 'btn-fitness':
        return api.plot_recent_fitness(players_df), {'display': 'block'}
    else:
        return no_update, no_update

# ------------------------ Table callback ----------------------------
@app.callback(
    Output('table-content', 'data'),
    Output('table-content', 'style_data_conditional'),
    Output('table-container', 'style'),
    Input('btn-lastseason', 'n_clicks'),
    Input('lastseason-radio', 'value'),
    Input('lastseason-slider', 'value'),
    State('app-data', 'data'),
    prevent_initial_call=True
)
def update_table(btn_lastseason, radio, slider, app_data):
    # Get data from session
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    players_df = pd.DataFrame(json.loads(app_data['players']))
    # Deliver desired info
    if trigger == 'btn-lastseason':
        data, styles = api.get_tops_from_last_season(players_df)
        return data, styles, {'display': 'block', 'margin': '1rem'}
    elif trigger in ['lastseason-radio', 'lastseason-slider']:
        # Deliver desired info
        position = radio
        bounds = slider
        data, styles = api.get_tops_from_last_season(players_df, position, bounds)
        return data, styles, {'display': 'block', 'margin': '1rem'}
    else:
        no_update, no_update, no_update


# ------------------------ Scoreboard callback ----------------------------
@app.callback(
    Output('scoreboard-content', 'data'),
    Output('scoreboard-content', 'style_data_conditional'),
    Output('scoreboard-container', 'style'),
    Input('btn-budget', 'n_clicks'),
    State('app-data', 'data'),
    State('budget-slider', 'value'),
    prevent_initial_call=True
)
def update_scoreboard(button, app_data, initial_budget):
    # Get data from session
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    market_df = pd.DataFrame(json.loads(app_data['market']))
    rounds_df = pd.DataFrame(json.loads(app_data['rounds']))
    if trigger == 'btn-budget':
        # Deliver desired info
        data, styles = api.show_scoreboard(initial_budget, market_df, rounds_df)
        return data, styles, {'display': 'block', 'margin': '1rem'}
    else:
        return no_update, no_update, no_update


# ------------------------ Run the app ----------------------------
if __name__ == '__main__':
    app.run_server(
        debug=False,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )