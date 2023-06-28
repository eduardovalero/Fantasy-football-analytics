import json
import requests
import pandas as pd
import plotly.express as px
from config import url
from time import strftime, localtime

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
        return pd.DataFrame.from_dict(players_json['data']['players'], orient='index')
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


def plot_budgets(initial_budget, market_df, rounds_df):

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
    # Estimate budget
    final_df = pd.DataFrame({
        'member': bonus_df.index.to_list(),
        'balance': (sell_df['amount'] - buy_df['amount'] + initial_budget*1e6 + bonus_df['bonus'])/1e6
    })
    fig = px.bar(final_df, x='member', y='balance', color='balance')

    return fig
