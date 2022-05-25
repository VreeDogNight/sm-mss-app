import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import requests
import pandas as pd # This is to allow converting data into pandas DataFrames to allow for easy data manipulation
import json
import dash_table # This is to display the data in Dash data Tables
import time # This is to delay the Meraki Api requests to 1 per second
import os # This is to remove the local file after it has been uploaded
import datetime # This is to create the date and time stamp to be put in the file name
from meraki_sdk.meraki_sdk_client import MerakiSdkClient # This is to get the Meraki Python SDK to work
from main_path import main_path


##################################################
# These are for the authorization to push the Firewall Rull Backup files to the Team Drive Folder
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
##################################################


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501


#This is setting up the Google Team Drive authentication.
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage(f'{main_path}/project_mssapp/slapdash/storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(f'{main_path}/project_mssapp/slapdash/app-credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

# This is the Google Team Drive folder where the firewall rules will be saved.
# frb = Firewall Rules Backup
frb_folder = 'Google Team Drive Folder'




# Functions
def list_all_networks_in_all_orgs():
    app.logger.info('Gathering list of all networks.')

    dataframe_network_list = pd.read_csv(f'{main_path}/project_mssapp/slapdash/current_meraki_networks.csv')

    combined_network_list = dataframe_network_list.to_dict('records')

    return combined_network_list



def search_for_network(network_data_frame, search_term):

    app.logger.info('starting general search for network')

    df = network_data_frame

    #Step-by-step explanation (from inner to outer):
    #df['name'] selects the name column of the data frame (techincally, the object df[name] is of type pandas.Series)
    #df['name'].str allows us to apply vectorized string methods (e.g., lower, contains) to the Series
    #df['name'].str.contains(user_search_input_1) checks each element of the Series as to whether the element value has the user search input string as a substring. The result is a Series of Booleans indicating True or False about the existence of a cell containing the search variable.
    #df[df['name'].str.contains(user_search_input_1)] applies the Boolean 'mask' to the dataframe and returns a view containing appropriate records.
    #na = False removes NA / NaN values from consideration; otherwise a ValueError may be returned.
    #.capitalize() will capitalize the first letter of the search string
    search_capitalized = df[df['name'].str.contains(search_term.capitalize(), na = False)]

    app.logger.debug('search_for_network() - ' + str(search_capitalized))

    #This will search using the variable user_search_input_1 as it was input by the user.
    search_lowercase = df[df['name'].str.contains(search_term, na = False, case=False)]

    app.logger.debug('search_for_network() - ' + str(search_lowercase))

    frames = [search_capitalized, search_lowercase]

    #This combines the 2 DataFrame responses
    results = pd.concat(frames).drop_duplicates()

    app.logger.debug('search_for_network() - ' + str(results))

    #This diplays just the name column as a list
    result_list = results['name'].tolist()

    app.logger.debug('search_for_network() - ' + str(result_list))

    app.logger.debug('search_for_network() - ' + str(len(result_list)))

    return result_list



def get_specific_network(network_data_frame, specific_network_name):
    app.logger.debug('starting search for specific network')

    df = network_data_frame

    #This will match the network name listed
    final_result = df[df['name'].str.match(specific_network_name, na = False)]

    app.logger.debug('get_specific_network() - ' + str(final_result))

    #This grabs the network ID as a list
    net_id_list = final_result['id'].tolist()

    app.logger.debug('get_specific_network() - ' + str(net_id_list))

    #This converts the network ID from a list to a string
    net_id_str = ''.join(net_id_list)

    app.logger.debug('get_specific_network() - ' + str(net_id_str))

    return net_id_str



def meraki_l3_frb(api_key, network_id, network_name):
    today_date_time = (str(datetime.datetime.now())).split('.')[0]

    app.logger.debug('meraki_l3_frb() - ' + str(today_date_time))

    client = MerakiSdkClient(api_key)

    mx_l3_firewall_controller = client.mx_l3_firewall

    result = mx_l3_firewall_controller.get_network_l3_firewall_rules(network_id)

    final_result = result[:-1]

    app.logger.debug('meraki_l3_frb() - ' + str(final_result))

    rules_df = pd.DataFrame(final_result)

    file_name_frb = network_name + ' ' + network_id + ' L3 Firewall Rules Backup ' + today_date_time + '.csv'

    app.logger.debug('meraki_l3_frb() - ' + str(file_name_frb))

    #This saves the Firewall Rules Backup information to a .csv file locally to this app
    rules_df.to_csv(f'{main_path}/project_mssapp/{file_name_frb}', index=False)

    body_dt = {'name': file_name_frb, 'mimeType': 'text/csv', 'parents': [frb_folder]}

    #This uploads the Firewall Rules Backup .txt file to a specified Google Team Drive Folder
    DRIVE.files().create(body=body_dt, media_body=f'{main_path}/project_mssapp/{file_name_frb}', supportsTeamDrives=True, fields='id').execute().get('id','parents')

    #This deletes the Firewall Rules Backup information .csv file
    os.remove(f'{main_path}/project_mssapp/{file_name_frb}')

    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Firewall Technician", "time_saved":"3", "note":"Backing up Meraki L3 Firewall Rules and saving to .csv file"}'

    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)

    app.logger.debug('Time saved for fulfillment (in minutes) - 3')

    return file_name_frb




# Layout
layout = html.Div([
    html.Div([
        html.H2('Firewall Rules Backup - Firewall Technicians'),
        html.P('This page will be used to backup the rules for a specific firewall, based on the name.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),

    html.Div([
        html.Div([
            html.H2('General Search Term'),
            dcc.Input(
                id='input-box-1_l3_firewall_rules_backup',
                type='text',
                placeholder='Search Term',
                value='')
        ], style={'margin-top': 30}),

        html.Div([
            html.H2('Meraki API Key'),
            dcc.Input(
                id='input-box-2_l3_firewall_rules_backup',
                type='text',
                placeholder='API Key',
                value='')
        ], style={'margin-top': 30}),

        html.Div([
            html.Button('Search', id='general_search_l3_firewall_rules_backup')
            ], style={'margin-top': 30})], className='ten columns offset-by-one'),

    html.Div(id='table_l3_firewall_rules_backup', className='six columns offset-by-three', style={'margin-top': 30}),
    html.Div(id='intermediate-value_l3_firewall_rules_backup', style={'display': 'none'})
])





# Callbacks
@app.callback(output=Output('intermediate-value_l3_firewall_rules_backup', 'children'),
    inputs=[Input('general_search_l3_firewall_rules_backup', "n_clicks")],
    state=[State('input-box-1_l3_firewall_rules_backup', "value")]
)
def get_combined_network_list(n_clicks, search_term):
    full_network_list = list_all_networks_in_all_orgs()

    if full_network_list == '':
        return 'error'

    else:
        network_df = pd.DataFrame(full_network_list)

        result_list = search_for_network(network_df, search_term)

        if len(result_list) == 0:
            return 'no results'

        else:
            network_search_df = pd.DataFrame(result_list)

            network_search_df.columns = ['Network']

            return [network_df.to_json(), network_search_df.to_json()]



@app.callback(Output('table_l3_firewall_rules_backup', 'children'), [Input('intermediate-value_l3_firewall_rules_backup', 'children')])
def networks_table(jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass

    else:
        if jsonified_cleaned_data == 'error':
            return html.H2('There was an error, please refresh the page and try again.')

        else:
            if jsonified_cleaned_data == 'no results':
                return html.H2('No Results were found. Please try a different search term.')

            else:
                networks = pd.read_json(jsonified_cleaned_data[1])
                return html.Div([
                        html.Div([
                            dash_table.DataTable(
                                id='datatable-interactivity_l3_firewall_rules_backup',
                                columns=[
                                    {"name": i, "id": i} for i in networks.columns
                                ],
                                data=networks.to_dict("rows"),
                                editable=False,
                                sort_action=True,
                                sort_mode="single",
                                row_selectable="multi",
                                selected_rows=[],
                                style_table={'margin-top': 10, 'overflowX': 'scroll'},
                                style_cell={
                                    'font-size': '12px',
                                    'text-align': 'center'
                                }
                            ),
                        ], className='twelve columns'),
                        html.Div([
                            html.Div(id='display_selected_row_l3_firewall_rules_backup', className='ten columns offset-by-one', style={'margin-top': 30})
                        ]),
                    ])



@app.callback(
    output=Output('display_selected_row_l3_firewall_rules_backup', "children"),
    inputs=[Input('datatable-interactivity_l3_firewall_rules_backup', "selected_rows")],
    state=[State('intermediate-value_l3_firewall_rules_backup', 'children'), State('datatable-interactivity_l3_firewall_rules_backup', "data")])
def update_table(selected_rows, jsonified_cleaned_data, rows):
    if jsonified_cleaned_data == None:
        pass
    else:
        networks = pd.read_json(jsonified_cleaned_data[1])
        # When the table is first rendered, `derived_virtual_data` and
        # `derived_virtual_selected_rows` will be `None`. This is due to an
        # idiosyncracy in Dash (unsupplied properties are always None and Dash
        # calls the dependent callbacks when the component is first rendered).
        # So, if `rows` is `None`, then the component was just rendered
        # and its value will be the same as the component's dataframe.
        # Instead of setting `None` in here, you could also set
        # `derived_virtual_data=fulfillment.to_rows('dict')` when you initialize
        # the component.
        if selected_rows is None:
            selected_rows = []

        if rows is None:
            dff = networks
        else:
            dff = pd.DataFrame(rows)

        dff = dff.iloc[selected_rows]

        if selected_rows == []:
            return ''
        else:
            if len(selected_rows) > 1:
                return html.Div([
                            html.Div(
                                dash_table.DataTable(
                                    id='display_selected_row_data_table_l3_firewall_rules_backup',
                                    columns=[
                                        {"name": i, "id": i} for i in networks.columns
                                    ],
                                    # data should be a list of dictionaries. [ {'column-1': 4.5, 'column-2': 'montreal', 'column-3': 'canada'}, {'column-1': 8, 'column-2': 'boston', 'column-3': 'america'} ]
                                    data=dff.to_dict("rows"),
                                    editable=False,
                                    style_table={'overflowX': 'scroll'},
                                    style_cell={
                                        'font-size': '12px',
                                        'text-align': 'center'
                                    }
                                )
                            ),
                            html.Div(
                                html.Div([
                                    html.H3('If these are the networks that you would like to back up the L3 firewall rules for, please press "Submit".'),
                                    html.Div(
                                        html.Button('Submit', id='specific_search_l3_firewall_rules_backup')
                                    ),
                                    html.Div(html.H4(id='output-container-button_l3_firewall_rules_backup'), style={'margin-top': 15})
                                ])
                            , className='twelve columns', style={'margin-top': 30})
                        ])
            else:
                return html.Div([
                            html.Div(
                                dash_table.DataTable(
                                    id='display_selected_row_data_table_l3_firewall_rules_backup',
                                    columns=[
                                        {"name": i, "id": i} for i in networks.columns
                                    ],
                                    # data should be a list of dictionaries. [ {'column-1': 4.5, 'column-2': 'montreal', 'column-3': 'canada'}, {'column-1': 8, 'column-2': 'boston', 'column-3': 'america'} ]
                                    data=dff.to_dict("rows"),
                                    editable=False,
                                    style_table={'overflowX': 'scroll'},
                                    style_cell={
                                        'font-size': '12px',
                                        'text-align': 'center'
                                    }
                                )
                            ),
                            html.Div(
                                html.Div([
                                    html.H3('If this is the network that you would like to back up the L3 firewall rules for, please press "Submit".'),
                                    html.Div(
                                        html.Button('Submit', id='specific_search_l3_firewall_rules_backup')
                                    ),
                                    html.Div(html.H4(id='output-container-button_l3_firewall_rules_backup'), style={'margin-top': 15})
                                ])
                            , className='twelve columns', style={'margin-top': 30})
                        ])



@app.callback(
    Output('output-container-button_l3_firewall_rules_backup', 'children'),
    [Input('specific_search_l3_firewall_rules_backup', 'n_clicks')],
    state=[State('datatable-interactivity_l3_firewall_rules_backup', "selected_rows"), State('intermediate-value_l3_firewall_rules_backup', 'children'), State('input-box-2_l3_firewall_rules_backup', "value")])
def update_output(n_clicks, rows, jsonified_cleaned_data, api_key):
    if jsonified_cleaned_data == None:
        pass
    else:
        networks = pd.read_json(jsonified_cleaned_data[0])
        selected_network = pd.read_json(jsonified_cleaned_data[1])

        if n_clicks == None:
            app.logger.debug('not searching for specific network yet')
            return ''
        else:
            x = 0

            list_specific_network_name = []

            list_l3_firewall_rules_backup_file = []

            for row in rows:
                app.logger.debug('searching for specific network')

                selected_row = (selected_network.iloc[[rows[x]]].to_dict("rows"))[0]

                app.logger.debug('selected row: ' + str(selected_row))

                specific_network_name = selected_row.get('Network', ' ')

                app.logger.debug('network name: ' + str(specific_network_name))

                network_id = get_specific_network(networks, specific_network_name)

                app.logger.debug('network ID: ' + str(network_id))

                l3_firewall_rules_backup_file = meraki_l3_frb(api_key, network_id, specific_network_name)

                list_specific_network_name.append(specific_network_name)

                list_l3_firewall_rules_backup_file.append(l3_firewall_rules_backup_file)

                app.logger.debug('##################################################')

                app.logger.debug(('The L3 Firewall rules for the location {} have been backed up in the file {} in the Google Team Drive.').format(list_specific_network_name, list_l3_firewall_rules_backup_file))

                app.logger.debug('##################################################')

                x += 1

            return ('The L3 Firewall rules for the location(s) {} have been backed up in the file(s) {} in the Google Team Drive.').format(list_specific_network_name, list_l3_firewall_rules_backup_file)
