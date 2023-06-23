
# ----------------------------- API variables -----------------------------

credentials = {
    'email': 'edpvalero@gmail.com',
    'password': '24204490aF:',
}

scenario = {
    'X-User': '7820380',
    'X-League': '512626'
}

url = {
    'login': 'https://biwenger.as.com/api/v2/auth/login',
    'market': 'https://biwenger.as.com/api/v2/league/',
    'players': 'https://cf.biwenger.com/api/v2/competitions/la-liga/data?lang=es&score=1&callback=jsonp_1465365482'
}


# ----------------------------- Layout variables -----------------------------

chart_info = {

    'payments': '''
               For all the members, display a distribution of the amounts that
               they have spent in player signings during the season.
               ''',

    'links': '''
              Show the flux of transactions between the members of 
              the league. Hover a particular link to display the number of 
              purchases between the two players connected by the link.
              ''',

    'signings': '''
               Display all the purchases performed by the members 
               of the league. For a particular player, hover to show the market
               value and the price paid by the member.
               ''',

    'performance': '''
              Show statistics that evaluate the performance of the
              players, like millions per point or goals per 90 minutes.
              ''',

    'budget': '''
                Select the initial budget in millions and the actual budget will be 
                calculated based on the history of transactions..
                '''
}

chart_titles = {
    'payments': 'How much do members pay to sign?',
    'links': 'How do members trade players?',
    'signings': 'History of signings',
    'budget': 'Which is the budget of the league members?',
    'performance': 'How do players perform?',
}

page_info = {

    'market': '''
            In this section, you can analyze the transactions made between
            the league members. The data processed here are gathered from 
            the start of the season to the present date.
            ''',

    'players': '''
               This page provides multiple tools to analyze players in the
               league. This includes ratios like points per game, points per 
               million, etc.
               '''
}

page_titles = {
    'market': 'Analyze the transactions made between the league members.',
    'players': 'Explore different performance metrics from La Liga players.'
}

page_suptitles = {
    'market': 'Market metrics',
    'players': 'Players performance'
}