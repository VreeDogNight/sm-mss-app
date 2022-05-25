import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import requests
import json


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501










layout = html.Div([
    html.Div([
        html.H2('Snipe-IT Quick Check In/Out'),
        html.P('This app will be used during the Snipe-IT asset data clean up and it will be retired after it is no longer needed. After entering in the "Asset Tag", the "Location Name", and the customer\'s "Internal ID" the app will go through and check in the device from the user and it will check it out to the location that was specified.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.Label('Asset Tag'),
        dcc.Input(id='input-1_page_1'),
    ], className='ten columns offset-by-one', style={'margin-top': 30}),

    html.Div([
        html.Label('Location Name'),
        dcc.Input(id='input-2_page_1'),
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.Label('Internal ID #'),
        dcc.Input(id='input-3_page_1'),
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.Button('Submit', id='button-2_page_1'),
    ], className='ten columns offset-by-one', style={'margin-top': 30}),

    html.Div([
        html.Div(id='output_page_1')
    ], className='ten columns offset-by-one', style={'margin-top': 10})
])










@app.callback(
    Output('output_page_1', 'children'),
    [Input('button-2_page_1', 'n_clicks')],
    state=[State('input-1_page_1', 'value'),
     State('input-2_page_1', 'value'),
     State('input-3_page_1', 'value')])
def compute(n_clicks, input1, input2, input3):
    if n_clicks == None:
        return 'Enter the Asset Tag, Location Name, and Internal ID #, then click Submit.'
    else:
        if input1 == None:
            return 'Error the "Asset Tag" field is blank.'
        else:
            if input2 == None:
                return 'Error the "Location Name" field is blank.'
            else:
                if input3 == None:
                    return 'Error the "Internal ID #" field is blank.'
                else:
                    asset_tag = input1

                    location_name = input2

                    internal_id = input3

                    name = 'internal_id_' + str(internal_id)

                    #print(name)

                    note = 'This is being checked in and then checked back out so that we can get a uniform format of data.'

                    url = "https://company.snipe-it.io/api/v1/hardware/"

                    payload = ""

                    api_key = 'api_key'

                    headers = {
                        'Content-Type': "application/json",
                        'Authorization': "Bearer " + api_key
                        }

                    response_asset_by_tag = requests.request("GET", url + "bytag/" + asset_tag, data=payload, headers=headers)

                    data = json.loads(response_asset_by_tag.text)

                    asset_id = str(data['id'])

                    #print(asset_id)

                    #data



                    # Set your server info
                    url_checkin = url + asset_id + '/checkin'

                    #print(url_checkin)

                    # Create the headers with your auth token
                    headers_checkin = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + api_key}

                    # Create a payload with the required fields
                    payload_checkin = {'note': note}

                    # Send the request and grab the response as a variable
                    response_checkin = requests.post(url_checkin, headers=headers_checkin, json=payload_checkin)

                    # print out the response, or you can do something meaningful with it.
                    print(response_checkin.text)



                    url_location = "https://company.snipe-it.io/api/v1/locations"

                    headers_location = {'Authorization':'Bearer ' + api_key, 'accept': 'application/json'}

                    params_location = (
                        ('search', location_name),
                    )

                    response_location = requests.request("GET", url_location, headers=headers_location, params=params_location)

                    #print(response_location.text)

                    data = json.loads(response_location.text)

                    location_id = data['rows'][0]['id']

                    #print(location_id)



                    # Set your server info
                    url_checkout = url + asset_id + '/checkout'

                    # Create the headers with your auth token
                    headers_checkout = {'Content-Type': 'application/json', 'Authorization':'Bearer ' + api_key}

                    # Create a payload with the required fields
                    payload_checkout = {'assigned_location': location_id, 'checkout_to_type': 'location', 'note': note, 'name': name}

                    # Send the request and grab the response as a variable
                    response_checkout = requests.post(url_checkout, headers=headers_checkout, json=payload_checkout)

                    # print out the response, or you can do something meaningful with it.
                    print(response_checkout.text)

                    print('')

                    print('The Asset: "{}" has been checked out to the Location: "{}", and was assigned the Internal ID # of "{}".'.format(input1, input2, input3))

                    print('')


                    return 'The Asset: "{}" has been checked out to the Location: "{}", and was assigned the Internal ID # of "{}".'.format(
                        input1, input2, input3
                    )
