import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501





# Functions





# Layout
layout = html.Div([
            html.Div([
                html.H2('Page Name - Using Team'),
                html.P('Description on page function.', style={'fontSize':14})
            ], className='ten columns offset-by-one', style={'margin-top': 10}),
            html.Div([
                html.Div([
                    html.Button('Refresh Orders', id='get_order_button_page_template')
                    ], style={'margin-top': 30})], className='ten columns offset-by-one'),
            html.Div(id='table_page_template'),
            html.Div([
                html.Div(id='display_selected_row_check_asset', className='ten columns offset-by-one')
            ]),
            html.Div(id='intermediate-value_page_template', style={'display': 'none'})
        ])





# Callbacks
@app.callback(
    Output('output-container-button_page_template', 'children'),
    # one Input
    [Input('button_page_template', 'n_clicks')],
    # list of State
    state=[State('radio_items_page_template', 'value'), State('datatable-interactivity_page_template', "selected_rows"), State('intermediate-page_template', 'children')])
def function_name(function, variables, go, here):
