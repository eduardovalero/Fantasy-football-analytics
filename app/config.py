from time import  strptime, mktime

# --------------------------------- API  -----------------------------------

url = {
    'login': 'https://biwenger.as.com/api/v2/auth/login',
    'market': 'https://biwenger.as.com/api/v2/league/',
    'players': 'https://cf.biwenger.com/api/v2/competitions/la-liga/data?lang=es&score=1&callback=jsonp_1465365482',
    'advanced': 'https://apim.laliga.com/public-service/api/v1/subscriptions/laliga-santander-2022/players/'
}


# ----------------------------------- Chart ---------------------------------
chart_titles = {
    'links': 'How do members trade players?',
    'budget': 'Balance of the league members',
    'performance': 'Player efficiency',
    'fitness': 'Recent player fitness',
    'lastseason': 'Last season top performances',
}

chart_info = {
    'links':
        '''
        Show the flux of transactions between league members.
        Hover a particular link to display the number of operations
        between the two members connected by the link.
        ''',
    'budget':
        '''
        Select the initial budget in millions and the actual budget will be 
        calculated based on the history of transactions.
        ''',
    'performance':
        '''
        Estimate player efficiency based on performance with respect
        to market value. Hover the players to view the exact values
        of this metric. 
        ''',
    'fitness':
        '''
        Visualize the fitness of the players during the last weeks.
        ''',
    'lastseason':
        '''
        Inspect the top players from last season in order to select
        potential target players for your current line up.
        '''
}

# ------------------------------ Pages in the app -----------------------------
page_suptitles = {
    'market': 'Market metrics',
    'players': 'Players performance'
}

page_titles = {
    'market': 'Analyze the transactions made between league members',
    'players': 'Explore different performance metrics from La Liga players'
}


page_info = {
    'market':
        '''
        In this page you can analyze the transactions made between
        the league members. The data processed here are gathered from 
        the start of the season to the present date.
        ''',
    'players':
        '''
        This page provides multiple tools to analyze players in the
        league. This includes ratios like points per game, points per 
        million, etc.
        '''
}


# ----------------------------------- Other ---------------------------------
epoch = int(mktime(strptime('23-07-2022 05:00:00', '%d-%m-%Y %H:%M:%S')))

