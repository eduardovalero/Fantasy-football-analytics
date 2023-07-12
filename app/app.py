import json
import pandas as pd
import dash.html as html
from layout import layout
import dash_bootstrap_components as dbc
from config import page_info, page_titles, page_suptitles, epoch
from dash import Dash, no_update, Input, Output, State, ctx
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
            # Enter demo mode when login form is not filled
            if not email and not password and not user and not league:
                app_data = {
                    'market': pd.read_excel('../data/market.xlsx').to_json(),
                    'rounds': pd.read_excel('../data/rounds.xlsx').to_json(),
                    'players': pd.read_excel('../data/players.xlsx').to_json(),
                    'advanced': pd.read_excel('../data/advanced.xlsx').to_json(),
                }
            # Else create a session and login
            else:
                session, token = api.login(email, password)
                # Request market data
                market_df, rounds_df = api.get_market(session, token, epoch, league, user)
                market_json = market_df.to_json()
                # Remove duplicates from rounds_df (this happens when a player performance is corrected)
                rounds_df.drop_duplicates(subset=['round', 'member'], inplace=True)
                rounds_json = rounds_df.to_json()
                # Request players data
                players_df = api.get_players(session)
                players_json = players_df.to_json()
                # Request advanced stats from La Liga
                advanced_df = api.get_advanced_stats(session)
                advanced_json = advanced_df.to_json()
                # Form app data dict
                app_data = {
                    'market': market_json,
                    'rounds': rounds_json,
                    'players': players_json,
                    'advanced': advanced_json
                }
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
    Output('chart-filter', 'style'),
    Input('btn-efficiency', 'n_clicks'),
    Input('btn-links', 'n_clicks'),
    Input('btn-fitness', 'n_clicks'),
    Input('btn-advanced', 'n_clicks'),
    Input('btn-chart-filter', 'n_clicks'),
    State('app-data', 'data'),
    State('chart-filter-input1', 'value'),
    State('chart-filter-input2', 'value'),
    prevent_initial_call=True
)
def update_chart(btn_efficiency, btn_links, btn_fitness, btn_advanced, btn_filter, app_data, name1, name2):
    # Get data from session
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    market_df = pd.DataFrame(json.loads(app_data['market']))
    players_df = pd.DataFrame(json.loads(app_data['players']))
    advanced_df = pd.DataFrame(json.loads(app_data['advanced']))
    # Deliver desired info
    if trigger == 'btn-efficiency':
        return api.plot_player_efficiency(players_df), {'display': 'block'}, {'display': 'none'}
    elif trigger == 'btn-links':
        return api.plot_links(market_df), {'display': 'block'}, {'display': 'none'}
    elif trigger == 'btn-fitness':
        return api.plot_recent_fitness(players_df), {'display': 'block'}, {'display': 'none'}
    elif trigger == 'btn-advanced':
        return {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
    elif trigger == 'btn-chart-filter':
        return api.plot_advanced(advanced_df, name1, name2), {'display': 'block'}, {'display': 'block'}
    else:
        return no_update, no_update


@app.callback(
    Output('chart-filter-list', 'children'),
    Input('chart-filter-radio', 'value'),
    State('app-data', 'data'),
    prevent_initial_call=True
)
def update_players(position, app_data):
    # Get data from session
    df = pd.DataFrame(json.loads(app_data['advanced']))
    # Filter data by position
    names = list(df.loc[df['position'] == position]['name'])
    # Output options based on names
    return [html.Option(value=name) for name in names]


@app.callback(
    Output('btn-chart-filter', 'disabled'),
    Input('chart-filter-input1', 'value'),
    Input('chart-filter-input2', 'value'),
    prevent_initial_call=True
)
def enable_player_filter(name1, name2):
    if name1 and name2:
        return False
    else:
        return True


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
        data, styles = api.get_table_lastseason(players_df)
        return data, styles, {'display': 'block', 'margin': '1rem'}
    elif trigger in ['lastseason-radio', 'lastseason-slider']:
        # Deliver desired info
        position = radio
        bounds = slider
        data, styles = api.get_table_lastseason(players_df, position, bounds)
        return data, styles, {'display': 'block', 'margin': '1rem'}
    else:
        no_update, no_update, no_update


# ------------------------ Scoreboard callback ----------------------------
@app.callback(
    Output('scoreboard-content', 'data'),
    Output('scoreboard-content', 'style_data_conditional'),
    Output('scoreboard-container', 'style'),
    Input('scoreboard-slider', 'value'),
    Input('app-data', 'data'),
    prevent_initial_call=True
)
def update_scoreboard(budget, app_data):
    '''
    Chained with login function via Input('app-data', 'data') so this
    callback can be triggered just after login, when 'app-data' is ready.

    This function creates and shows the league scoreboard upon login.
    '''
    # Get data from session
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    market_df = pd.DataFrame(json.loads(app_data['market']))
    rounds_df = pd.DataFrame(json.loads(app_data['rounds']))
    # Deliver desired info
    if trigger == 'app-data':
        show = {'display': 'block', 'margin': '1rem'}
        data, styles = api.show_scoreboard(20, market_df, rounds_df)
    elif trigger == 'scoreboard-slider':
        show = {'display': 'block', 'margin': '1rem'}
        data, styles = api.show_scoreboard(budget, market_df, rounds_df)
    else:
        data, styles, show = no_update, no_update, no_update
    # Output
    return data, styles, show


# ------------------------ Run the app ----------------------------
if __name__ == '__main__':
    app.run_server(
        debug=False,
        dev_tools_ui=False,
        dev_tools_props_check=False
    )