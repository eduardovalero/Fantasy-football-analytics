import json
import requests
import pandas as pd
from config import scenario, url, credentials
from time import strftime, strptime, localtime, mktime

def login(s):
    '''
    Logs in to Biwenger using the credentials set in config.py

    :param s: requests session created by main loop.
    :return: session token generated upon login.
    '''

    # Login with credentials
    post = s.post(url['login'], data=credentials)

    # Return token
    if post.status_code == 200:
        return post.json()['token']
    else:
        raise Exception(f'Cannot login! Status code = {post.status_code}')


def get_players(s):
    '''
    Gets all the players in the app as a table.

    :param s: requests session created by main loop.
    :return: all the players table.
    '''

    # Get players
    players = s.get(url=url['players'])
    players_json = json.loads(players.text.split('(', 1)[1].strip(')'))

    # Create the players table
    if players_json['status'] == 200:
        players_df = pd.DataFrame.from_dict(players_json['data']['players'], orient='index')
    else:
        raise Exception(f'Error getting list of players. Status code: {players_json["status"]}')
    return players_df


def get_market(s, token):
    '''
    Gets the players offered in the market as a table.

    :param s: requests session created by main loop.
    :param token: session token generated upon login.
    :return: market players table.
    '''

    # Get market
    market = s.get(
        url=url['market'],
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'X-League': scenario['X-League'],
            'X-User': scenario['X-User']
        }
    )

    # Create the market table
    market_json = market.json()
    if market_json['status'] == 200:
        market_df = pd.DataFrame.from_dict(market_json['data']['sales'])
    else:
        raise Exception(f'Error getting players in the market. Status code: {market_json["status"]}')
    return market_df


def get_home(session, token, start):

    limit = 200
    offset = 0
    sales_list = list()

    # Request data until start date
    while True:

        # Get home page board
        home = session.get(
            url=url['home'] + f'{scenario["X-League"]}/board?offset={offset}&limit={limit}',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
                'X-League': scenario['X-League'],
                'X-User': scenario['X-User']
            }
        )

        # Extract market and transfer sales
        for news in home.json()['data']:
            if news['date'] < start:
                return pd.DataFrame.from_dict(sales_list)
            else:
                if news['type'] == 'market':
                    for event in news['content']:
                        sales_list.append(dict(
                            player=event['player'],
                            seller='market',
                            buyer=event['to']['name'],
                            amount=event['amount'],
                            date=strftime('%d-%m-%Y %H:%M:%S', localtime(news['date'])))
                        )
                elif news['type'] == 'transfer':
                    for event in news['content']:
                        sales_list.append(dict(
                            player=event['player'],
                            seller=event['from']['name'],
                            buyer=event['to']['name'] if 'to' in event.keys() else 'market',
                            amount=event['amount'],
                            date=strftime('%d-%m-%Y %H:%M:%S', localtime(news['date'])))
                        )
                else:
                    pass

        # Update offset for next request
        offset += limit


if __name__ == '__main__':
    with requests.Session() as s:
        # Log in website
        token = login(s)
        # Get players list
        players_df = get_players(s)
        # Get market sales
        market_df = get_market(s, token)
        # Get transfers
        date = '23-07-2022 05:00:00'
        format = '%d-%m-%Y %H:%M:%S'
        epoch = int(mktime(strptime(date, format)))
        home_df = get_home(s, token, epoch)
        home_df.to_excel('sales.xlsx')