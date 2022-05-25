import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501


layout = html.Div([
    html.Div([
        html.H2('Retired Apps'),
        html.P('This is where any apps that are no longer needed will go so that they are out of the way but can still be used.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),
    html.Div([
        html.H1('There are currently no apps that have been retired and are no longer in active use.'),
    ], className='ten columns offset-by-one', style={'margin-top': 30}),
])
