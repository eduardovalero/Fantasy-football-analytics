from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)