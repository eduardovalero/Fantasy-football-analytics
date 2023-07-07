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
    'performance': 'Player efficiency',
    'fitness': 'Recent player fitness',
    'lastseason': 'Last season top performances',
    'advanced': 'Advanced game stats'
}

chart_info = {
    'links':
        '''
        Show the flux of transactions between league members.
        Hover a particular link to display the number of operations
        between the two members connected by the link.
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
        ''',
    'advanced':
        '''
        Compare players using advanced statistics provided by La Liga.
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

css = dict(
    font = 'system-ui',
    color_body = '#1F2833',
    color_navbar = '#1A1A1E',
    color_title = '#66FCF1',
    color_subtitle = '#E3E2DF',
    color_text = '#E3E2DF',
    color_button = '#45A29E'
)

epoch = int(mktime(strptime('23-07-2022 05:00:00', '%d-%m-%Y %H:%M:%S')))

chart_options = dict(
    font = {'size': 16, 'family': 'system-ui', 'color': '#E3E2DF'},
    height = 750,
    paper_bgcolor = '#1F2833',
    plot_bgcolor = '#1F2833',
    xaxis = {'gridwidth': 1, 'gridcolor': '#E3E2DF'},
    yaxis = {'gridwidth': 1, 'gridcolor': '#E3E2DF'}
)

advanced_stats = dict(
    defender = [
        'games_played',
        'yellow_cards'
        'total_red_cards',
        'total_clearances',
        'duels_won'
    ],
    midfielder = [
        'games_played',
        'yellow_cards',
        'successful_open_play_passes',
        'goal_assists',
        'goals'
    ],
    forward = [
        'games_played',
        'successful_dribbles',
        'goal_assists',
        'shots_on_target_inc_goals',
        'goals'
    ]
)

laliga_map = dict(
    Portero = 'keeper',
    Defensa = 'defender',
    Centrocampista = 'midfielder',
    Delantero = 'forward'
)

spinner_dict = dict(
    fullscreen = True,
    color = 'primary',
    spinner_style = {'width': '5rem', 'height': '5rem'},
    fullscreen_style = {'opacity': '0.5', 'z-index': '999999'}
)

slider_dict = dict(
    marks = None,
    tooltip = {"placement": "bottom", "always_visible": True}
)

style_data = dict(
    textAlign = 'center',
    fontFamily = css['font'],
    backgroundColor = css['color_body'],
    color = css['color_text']
)

style_header = dict(
    textAlign = 'center',
    fontFamily = css['font'],
    backgroundColor = css['color_navbar'],
    color = css['color_title']
)

positions = ['keeper', 'defender', 'midfielder', 'forward']