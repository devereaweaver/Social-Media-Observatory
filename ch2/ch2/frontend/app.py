# Instantiate Dash app and route requests for different pages of app
from dash import Dash, dcc, html, Input, Output
import dash

import secrets
from .pages import welcome, upload   

# Instantiate a Dash objeect
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
server.secret_key = secrets.token_hex()

# Define the page's HTML layout for visual rendering 
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ]
)

# Write callback to define nhow the app should respond to user interaction with 
# the HTML content
@dash.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    """
    Takes as input the pathname of any URL entered by the investigator in the 
    web browser, and returns an appropriate page layout.
    """
    if pathname == '/':
        return welcome.layout
    elif pathname == '/upload':
        return upload.layout
    else:
        return "404"

def run():
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':     
    run()