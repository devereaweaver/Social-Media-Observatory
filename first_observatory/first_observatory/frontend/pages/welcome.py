# Landing page, if user clicks on /upload enpoint, the click 
# will trigger callback in app.py and redirect them to the 
# /upload page defined in upload.py
from dash import dcc, html

layout = html.Div(
    [
        html.Div(
            [
                html.H1("Welcome to the Social Meida Observatory"),
                dcc.Link("Upload Telegram Handles", href="/upload"),
            ]
        )
    ]
)