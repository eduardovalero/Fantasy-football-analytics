from dash import Dash
from layout import layout
from dash import Input, Output
import dash_bootstrap_components as dbc
from config import page_info, page_titles, page_suptitles


# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = layout

# App callbacks
@app.callback(
    Output("sidebar-suptitle", "children"),
    Output("sidebar-title", "children"),
    Output("sidebar-info", "children"),
    Output("market-accordion", "style"),
    Output("player-accordion", "style"),
    Input("url", "pathname")
)
def update_accordion(path):
    print(path)
    if path == "/":
        return page_suptitles['market'], page_titles['market'], page_info["market"], {"display": "block"}, {"display": "none"}
    elif path == "/players":
        return page_suptitles['players'], page_titles['players'], page_info["players"], {"display": "none"}, {"display": "block"}
    else:
        pass


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)