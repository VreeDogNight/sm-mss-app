import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501


layout = html.Div([
    html.Div([
        html.H1('MSS App'),
        html.P('This app will be used by the MSS department to help speed up everyday tasks, to  increase efficiency and reduce required work.', style={'fontSize':18})
    ], className='ten columns offset-by-one', style={'margin-top': 30}),

    html.Div([
        html.H2('Check Asset - Fulfillment Team'),
        html.P('After an order has come in, this will be used to check the accuracy of the information from sales before the information is sent to the webhooks.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Assign Asset - Fulfillment Team'),
        html.P('After an order has been approved, this will be used to assign devices to customer locations in Snipe-IT as well as claim the device to the correct Meraki network(if applicable).', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Ship Asset - Fulfillment Team'),
        html.P('After a device has been taken upstairs to be shipped, this will be used to update the shipdate in Snipe-IT.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Find Meraki Network ID - Firewall Technicians'),
        html.P('This page can be used to find a Meraki Network ID based on the name.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Firewall Rules Backup - Firewall Technicians'),
        html.P('This page will be used to backup the rules for a specific firewall, based on the name.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Firewall Rules Upload - Firewall Technicians'),
        html.P('This page will be used to upload a new ruleset for a specific firewall, based on the name, using a .csv file.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Firewall Rules Append CSV - Firewall Technicians'),
        html.P('This page will be used to append additional rules for a specific firewall, based on the name, using a .csv file.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Firewall Rules Manually Add - Firewall Technicians'),
        html.P('This page will be used to manually add additional rules for a specific firewall, based on the name.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Update Inventory Manager Spreadsheet'),
        html.P('This will be used to update the \'Inventory Manager\' with the current inventory information from the Snipe-IT database.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Snipe-IT Quick Check In/Out'),
        html.P('This app will be used during the Snipe-IT asset data clean up and it will be retired after it is no longer needed. After entering in the "Asset Tag", the "Location Name", and the customer\'s "Internal ID" the app will go through and check in the device from the user and it will check it out to the location that was specified.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.H2('Retired Apps'),
        html.P('This is where any apps that are no longer needed will go so that they are out of the way but can still be used.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

])
