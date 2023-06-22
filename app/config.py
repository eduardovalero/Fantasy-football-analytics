
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

    'boxplot': '''
               For all the members, display a distribution of the amounts that
               they have spent in player signings during the season.
               ''',

    'sankey': '''
              This chart shows the flux of transactions between the members of 
              the league. Hover a particular link to display the number of 
              purchases between the two players connected by the link.
              ''',

    'scatter': '''
               This chart displays all the purchases performed by the members 
               of the league. For a particular player, hover to show the market
               value and the price paid by the member.
               ''',

    'bubble': '''
              This chart shows statistics that evaluate the performance of the
              players.
              '''
}

chart_titles = {
    'boxplot': 'How much do members pay to sign?',
    'sankey': 'How do members trade players?',
    'scatter': 'History of signings',
    'bubble': 'How do players perform?',
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
               million, etc. This is useful to find most profitable and 
               effective players, among other things.

               Upload a players.csv file to run analytics.
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

market_guide = '''
               Click the 'Market' tab in the header of the app. Then, 
               drag and drop the Excel file containing all the market
               information. Lastly, select the chart you want to 
               display from the menu and click 'Display'. You can interact 
               with the charts using the controls in the top-right corner.
               '''

player_guide = '''
               Click the 'Players' tab in the header of the app. Then,
               drag and drop the Excel file containing all the information 
               about the players in the League. Finally, select the chart you 
               want to display from the menu and click 'Display'. As with the 
               market analytics, you can interact with the charts using the 
               controls showed in the top-right corner.
               '''