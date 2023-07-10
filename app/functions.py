import json
import requests
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
from time import strftime, localtime
from plotly.express.colors import sample_colorscale
from config import url, chart_options, advanced_stats, laliga_map


# ------------------------------------- API ----------------------------------------

def login(email, password):
    '''
    Logs in to Biwenger using the credentials set in config.py

    :param email: the email to login to Biwenger.
    :param password: the password to login to Biwenger.
    :return: session token generated upon login.
    '''

    # Open HTTP session
    with requests.Session() as session:

        # Login with credentials
        post = session.post(url['login'], data={'email': email, 'password': password})

        # Return token
        if post.status_code == 200:
            return session, post.json()['token']
        else:
            raise Exception(f'Cannot login! Status code = {post.status_code}')


def get_players(session):
    '''
    Gets all the players in the app as a table.

    :param session: requests session created by main loop.
    :return: all the players table.
    '''

    # Get players
    players = session.get(url=url['players'])
    players_json = json.loads(players.text.split('(', 1)[1].strip(')'))

    # Create the players table
    if players_json['status'] == 200:
        # Create dataframe
        df = pd.DataFrame.from_dict(players_json['data']['players'], orient='index')
        df['played'] = df['playedHome'] + df['playedAway']
        df.replace({'position': {1: 'keeper', 2: 'defender', 3: 'midfielder', 4: 'forward', 5: 'trainer'}}, inplace=True)
        # Calculate total points for recent fitness
        df['fitness_total'] = df['fitness'].apply(lambda x: sum([score if isinstance(score, int) else 0 for score in x]))
        # Drop players who did not perform
        df.drop(labels=df[df['points'] <= 0].index, inplace=True)
        df.drop(labels=df[df['played'] <= 0].index, inplace=True)
        # Estimate points/game and points/million
        df['points_per_game'] = df['points'] / df['played']
        df['points_per_mill'] = df['points'] / (df['price'] / 1e6)
        return df
    else:
        raise Exception(f'Error getting list of players! Status code: {players_json["status"]}')


def get_market(session, token, epoch, league, user):
    '''
    Gets all transfers completed from the date passed in epoch.
    The transfer list is returned as a table.

    :param session: requests session created by main loop.
    :param token: session token generated upon login.
    :param epoch: date from which to collect transfers.
    :param league: the id of the league.
    :param user: the id of the player.
    :return: transfers table.
    :return: round bonus table.
    '''

    limit = 200
    offset = 0
    sales_list = list()
    round_list = list()

    # Request data until start date
    while True:

        # Get home page board
        home = session.get(
            url=url['market'] + f'{league}/board?offset={offset}&limit={limit}',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
                'X-League': league,
                'X-User': user
            }
        )

        # Extract market and transfer sales
        for news in home.json()['data']:
            if news['date'] < epoch:
                return pd.DataFrame.from_dict(sales_list), pd.DataFrame.from_dict(round_list)
            else:
                if news['type'] == 'market':
                    for event in news['content']:
                        sales_list.append(dict(
                            player_id=event['player'],
                            seller='market',
                            buyer=event['to']['name'],
                            amount=event['amount'],
                            date=strftime('%d-%m-%Y %H:%M:%S', localtime(news['date'])))
                        )
                elif news['type'] == 'transfer':
                    for event in news['content']:
                        sales_list.append(dict(
                            player_id=event['player'],
                            seller=event['from']['name'],
                            buyer=event['to']['name'] if 'to' in event.keys() else 'market',
                            amount=event['amount'],
                            date=strftime('%d-%m-%Y %H:%M:%S', localtime(news['date'])))
                        )
                elif news['type'] == 'roundFinished':
                    for event in news['content']['results']:
                        round_list.append(dict(
                            round=news['content']['round']['name'],
                            member=event['user']['name'],
                            points=event['points'] if 'bonus' in event.keys() else 0,
                            bonus=event['bonus'] if 'bonus' in event.keys() else 0)
                        )
                else:
                    pass

        # Update offset for next request
        offset += limit


def get_advanced_stats(session):

    # HTTP request variables
    limit = 100
    offset = 0
    players = list()

    while True:
        # Request batch of the players
        stats = session.get(
            url = url['advanced'] + f'stats?limit={limit}&offset={offset}&orderField=name&orderType=ASC',
            headers={"ocp-apim-subscription-key": "c13c3a8e2f6b46da9c5c425cf61fab3e"},
        )
        # While data is returned
        if stats.json():
            if stats.status_code == 200:
                # Append returned data
                players.append(stats.json()['player_stats'])
                offset += 100
            else:
                raise Exception(f'Stats | Status code = {stats.status_code}')
        # When all data have been returned
        else:
            # Flatten gathered list
            players = [item for sublist in players for item in sublist]
            # Create dataframe
            df = pd.DataFrame(players)
            # Explode stats into columns
            df = pd.concat(
                objs=[
                    df.drop('stats', axis=1),
                    pd.DataFrame(
                        [{x['name']: x['stat'] for x in row} for row in
                         df['stats']])],
                axis=1
            )
            # Fill NaNs with zeroes
            df.fillna(value=0, inplace=True)
            # Map name of positions between LaLiga and Football fantasy
            df['position'] = df['position'].apply(lambda x: laliga_map[x['name']] if x else 'undefined')
            return df


# ----------------------------- Data analysis --------------------------------------

def show_scoreboard(initial_budget, market_df, rounds_df):
    '''
    Creates a table showing the economic balance and current poitns of the
    league members.

    :param initial_budget: initial budget in (€) millions set by the league.
    :param market_df: market dataframe.
    :param rounds_df: rounds dataframe.
    :return: data to show in the table as a dict.
    '''

    # Sells per member
    sell_df = market_df.groupby('seller')['amount'].sum().reset_index()
    sell_df.drop(sell_df.loc[sell_df['seller'] == 'market'].index, inplace=True)
    sell_df.set_index('seller', inplace=True)
    # Buys per member
    buy_df = market_df.groupby('buyer')['amount'].sum().reset_index()
    buy_df.drop(buy_df.loc[buy_df['buyer'] == 'market'].index, inplace=True)
    buy_df.set_index('buyer', inplace=True)
    # Bonuses per member
    bonus_df = rounds_df.groupby('member', as_index=False)['bonus'].sum()
    bonus_df.set_index('member', inplace=True)
    # Points per member
    points_df = rounds_df.groupby('member', as_index=False)['points'].sum()
    points_df.set_index('member', inplace=True)
    # Estimate budget
    final_df = pd.DataFrame({
        'member': bonus_df.index.to_list(),
        'points': points_df['points'],
        'balance': (sell_df['amount'] - buy_df['amount'] + initial_budget*1e6 + bonus_df['bonus'])/1e6
    })
    # Get color scale for the balance column
    styles = discrete_background_color_bins(df=final_df, columns=['balance'])

    return final_df.to_dict('records'), styles


def plot_player_efficiency(players_df):
    '''
    Plots a scatter plot with the effiency of the players.

    :param players_df: players dataframe.
    :return: scatter plot.
    '''

    # Process data
    df = players_df.copy()
    # Create figure
    fig = px.scatter(
        data_frame=df, x='points_per_game', y='points_per_mill',
        size='points', color='position', hover_name='name',
        labels={
            'points_per_game': 'Points per game',
            'points_per_mill': 'Points per million',
            'position': 'Position',
            'points': 'Points'},
    )
    # Update layout
    fig.update_layout(
        title={'text': 'Player efficiency', 'x': 0.5, 'y': 0.95},
        **chart_options
    )
    return fig


def plot_links(market_df):
    '''
    Renders a chord chart displaying financial transactions
    between league members.

    :param market_df: market dataframe
    :return: sankey diagram.
    '''
    # Process data
    df = market_df.copy()
    # Get transactions between league members
    grouped = df.groupby(by=['seller', 'buyer'], dropna=False)
    grouped = grouped.player_id.count().unstack(fill_value=0)
    # Drop market transactions
    grouped.drop(labels='market', axis=0, inplace=True)
    grouped.drop(labels='market', axis=1, inplace=True)
    # Create numpy array for the chart
    data = grouped.to_numpy()
    # Format data for sankey diagram
    members = list(grouped.columns)
    label = members * 2
    source = np.repeat(list(range(0, len(members))), len(members))
    target = list(range(len(members), len(members) * 2)) * len(members)
    value = data.reshape((-1, 1))
    # Data to dict, dict to Sankey
    color = sns.color_palette('deep').as_hex()[:len(members)]
    color_node = color * 2
    link = {'source': source, 'target': target, 'value': value}
    node = {'label': label, 'pad': 50, 'thickness': 10, 'color': color_node}
    sankey = go.Sankey(link=link, node=node)
    # Create figure
    fig = go.Figure(data=sankey)
    fig.update_layout(
        title={'text': 'Member financial links', 'x': 0.5, 'y': 0.95},
        **chart_options
    )
    return fig


def plot_recent_fitness(players_df):
    '''
    Plots a scatter plot with the recent fitness of the players.

    :param players_df: players dataframe.
    :return: scatter plot with recent fitness.
    '''

    # Process data
    df = players_df.copy()
    # Create figure
    fig = px.scatter(
        data_frame=df, x='fitness_total', y='price',
        size='points', color='position', hover_name='name',
        labels={'position': 'Position', 'fitness': 'fitness_total'})
    # Update layout
    fig.update_layout(
        title={'text': 'Player recent fitness', 'x': 0.5, 'y': 0.95},
        **chart_options
    )
    return fig


def plot_advanced(advanced_df, name1, name2):
    '''
    Plots a radar chart displaying advanced statistics of two players
    whose names are provided as input parameters. The statistics are
    selected based on the position of the two players.

    :param advanced_df: advanced stats dataframe from La Liga.
    :param name1: name of player 1.
    :param name2: name of player 2.
    :return: radar plot.
    '''

    # Process data
    df = advanced_df.copy()
    pos = df.loc[df['name'] == name1]['position'].values[0]
    stats = advanced_stats[pos]
    df = df.loc[df['name'].isin([name1, name2])][['name', 'position'] + stats]
    # Chart ranges
    ranges = list(df[stats].max().values)
    metrics = [x.replace('_', ' ').capitalize() for x in stats]
    labels = [metric_i + f' ({range_i})' for metric_i, range_i in zip(metrics, ranges)]
    # Loop players to plot
    fig = go.Figure()
    for index in range(len(df)):
        # Scale all plot axis so the chart is interpretable
        values = list(df.iloc[index][stats])
        scaled = [round(value_i / range_i, 2) if range_i != 0 else range_i for value_i, range_i in zip(values, ranges)]
        # Plot player
        fig.add_trace(go.Scatterpolar(
            r=scaled,
            theta=labels,
            fill='tonext',
            name=df.iloc[index]['name']
            )
        )
    fig.update_layout(
        title={'text': 'Advanced player statistics', 'x': 0.5, 'y': 0.95},
        polar=dict(bgcolor = chart_options['paper_bgcolor'], radialaxis={'visible': True, 'range': [0, 1]}),
        showlegend=False,
        **chart_options
    )

    return fig


def get_table_lastseason(players_df, position='forward', bounds=[0, 100], N=10):
    # Columns to keep
    cols = ['name', 'position', 'status', 'price', 'pointsLastSeason']
    df = players_df[cols].copy()
    # Segment data
    df_pos = df.loc[(df['position'] == position) & (bounds[0]*1e6 <= df['price']) & (df['price'] <= bounds[1]*1e6)]
    df_pos = df_pos.sort_values(by=['pointsLastSeason'], ascending=False)
    df_pos.drop(labels='position', axis=1, inplace=True)
    df_pos.reset_index(drop=True, inplace=True)
    df_pos_top = df_pos.loc[0:N-1]
    # Get table styles
    styles = discrete_background_color_bins(df=df_pos_top, columns=['pointsLastSeason'])

    return df_pos_top.to_dict('records'), styles


def discrete_background_color_bins(df, columns, n_bins=7):
    '''
    Colors each cell in the table according to their value. This
    function was copied from the plotly official documentation:
    https://dash.plotly.com/datatable/conditional-formatting
    #highlighting-cells-by-value-with-a-colorscale-like-a-heatmap

    :param df: dataframe containing the table info.
    :param n_bins: number of bins to consider.
    :param columns: columns to apply the coloring.
    :return: style to apply to the dash table.
    '''

    # Segment data
    df_use = df[columns]

    # Select colors from scale
    sample = np.linspace(0, 1, len(df) + 1)
    colors = list(reversed(sample_colorscale(colorscale='Greens', samplepoints=list(sample))))
    bounds = np.linspace(0, 1, len(df) + 1)

    # Define ranges
    df_max = df_use.max().max()
    df_min = df_use.min().min()
    ranges = [((df_max - df_min) * i) + df_min for i in bounds]
    styles = list()

    # Assign colors to cell
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colors[i - 1]
        color = 'inherit' if i > len(bounds) / 2. else 'white'
        for column in df_use:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })

    return styles