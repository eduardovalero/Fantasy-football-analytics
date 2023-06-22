import json
import requests
import pandas as pd
from config import scenario, url, credentials
from time import strftime, strptime, localtime, mktime

def login(session):
    '''
    Logs in to Biwenger using the credentials set in config.py

    :param session: requests session created by main loop.
    :return: session token generated upon login.
    '''

    # Login with credentials
    post = session.post(url['login'], data=credentials)

    # Return token
    if post.status_code == 200:
        return post.json()['token']
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


def get_home(session, token, epoch):
    '''
    Gets all transfers completed from the date passed in epoch.
    The transfer list is returned as a table.

    :param session: requests session created by main loop.
    :param token: session token generated upon login.
    :param epoch: date from which to collect transfers.
    :return: transfers table.
    '''

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
            if news['date'] < epoch:
                return pd.DataFrame.from_dict(sales_list)
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
        players_df.to_excel('./data/players.xlsx')
        # Get transfers from a specific date
        epoch = int(mktime(strptime('23-07-2022 05:00:00', '%d-%m-%Y %H:%M:%S')))
        home_df = get_home(s, token, epoch)
        # Insert column with player id and fill players who left the competition
        home_df.insert(loc=1, column='player_name', value=home_df['player_id'].map(players_df.set_index('id')['name']))
        home_df['player_name'].fillna(value='Missing', inplace=True)
        home_df.to_excel('data/sales.xlsx')