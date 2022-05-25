import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from gspread_pandas import Spread
import dash_table
import requests
import json
import datetime
import gspread_pandas
from main_path import main_path


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501



#This sets the creds to come from the 'google_secret.json' file that is in the repo with the app
creds = gspread_pandas.conf.get_config(conf_dir=f'{main_path}/project_mssapp/', file_name='google_secret.json')



def update_asset(asset_serial, ship_date):

    app.logger.info('searching for asset ID in Snipe-IT by serial number')

    url = "https://company.snipe-it.io/api/v1/hardware/"

    snipeit_api_key = 'snipeit_api_key'

    payload_search = ""

    headers_search = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipeit_api_key
    }

    app.logger.debug('Asset being searched for: ' + asset_serial)

    response_asset_by_serial = requests.request("GET", url + "byserial/" + asset_serial, data=payload_search, headers=headers_search)

    app.logger.debug('Asset search response data: ' + response_asset_by_serial.text)

    data = json.loads(response_asset_by_serial.text)

    asset_id = str(data['rows'][0]['id'])

    app.logger.debug('Asset ID: ' + str(asset_id))

    url_update = url + asset_id

    payload_update = '_snipeit_date_shipped_6=' + str(ship_date) + '&undefined='

    headers_update = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipeit_api_key
    }

    response_update = requests.request("PUT", url_update, data=payload_update, headers=headers_update)

    app.logger.debug('Asset update response data: ' + response_update.text)


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", "time_saved":"1", "note":"MSS App updating shipping date for asset in Snipe-IT"}'

    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)


    app.logger.debug('Time saved for fulfillment (in minutes) - 1')

    return response_update.text



def update_master_gsheet(created_at, sales_agent, ship_date):
    time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    #This sets the spreadsheet that the code will be working with.
    s_start = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)

    app.logger.debug(s_start)

    app.logger.debug(s_start.sheets)

    #This sets the worksheet in the spreadsheet that the code will be working with.
    data_sheet_start = 'Name of worksheet'

    app.logger.debug(s_start.url)

    #This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)

    #This converts the contents of the worksheet to be a pandas DataFrame so that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    #df_start

    for index, row in df_start.iterrows():
        if row['Created At'] == created_at:
            if row['Sales Agent'] == sales_agent:
                row_number = str(row.name + 2)
                new_row_data = [
                    'Shipped',
                    row['Created At'],
                    row['Internal ID'],
                    row['Invoice #'],
                    row['Customer Email'],
                    row['Sales Agent'],
                    row['Processing Bank'],
                    row['First Name'],
                    row['Last Name'],
                    row['Company Name'],
                    row['Phone Number'],
                    row['Ship Address'],
                    row['Ship City'],
                    row['Ship State'],
                    row['Ship Zip'],
                    row['Ship Country'],
                    row['Install Address'],
                    row['Install City'],
                    row['Install State'],
                    row['Install Zip'],
                    row['Install Country'],
                    row['Upgrade Response'],
                    row['Fulfillment Type'],
                    row['Firewall Model'],
                    row['Latitude'],
                    row['Longitude'],
                    row['Serial #'],
                    row['Tracking #'],
                    row['Not Checked'],
                    row['Checked'],
                    row['Assigned'],
                    ship_date,
                    row['Delivered'],
                    row['Online'],
                    row['Notes'],
                    row['Sale Type'],
                ]
                s_start.update_cells(start=(str('A' + row_number)), end=(str('AJ' + row_number)), vals=new_row_data)
        else:
            pass

    return ''










layout = html.Div([
            html.Div([
                html.H2('Ship Asset - Fulfillment Team'),
                html.P('After a device has been taken upstairs to be shipped, this will be used to update the shipdate in Snipe-IT.', style={'fontSize':14})
            ], className='ten columns offset-by-one', style={'margin-top': 10}),
            html.Div([
                html.Div([
                    html.Button('Refresh Orders', id='get_order_button_ship_asset')
                    ], style={'margin-top': 30})], className='ten columns offset-by-one'),
            html.Div(id='table_ship_asset'),
            html.Div([
                html.Div(id='display_selected_row_ship_asset', className='ten columns offset-by-one')
            ]),
            html.Div(id='intermediate-value_ship_asset', style={'display': 'none'})
        ])










@app.callback(output=Output('intermediate-value_ship_asset', 'children'),
    inputs=[Input('get_order_button_ship_asset', "n_clicks")])
def get_order_data(n_clicks):

    app.logger.info('Ship Asset Refreshing Orders...')

    #This sets the spreadsheet that the code will be working with.
    s_start = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)
    #s

    #s.sheets

    #This sets the worksheet in the spreadsheet that the code will be working with.
    data_sheet_start = 'Name of worksheet'

    #s.url

    #This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)
    #s

    #This converts the contents of the worksheet to be a pandas DataFrame so that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    filtered_list = df_start.loc[df_start['Status'] == 'Assigned']

    fulfillment = pd.DataFrame()

    fulfillment['Status'] = filtered_list['Status']

    fulfillment['Created At'] = filtered_list['Created At']

    fulfillment['Internal ID'] = filtered_list['Internal ID']

    fulfillment['Invoice #'] = filtered_list['Invoice #']

    fulfillment['Processing Bank'] = filtered_list['Processing Bank']

    fulfillment['Customer Email'] = filtered_list['Customer Email']

    fulfillment['Sales Agent'] = filtered_list['Sales Agent']

    fulfillment['First Name'] = filtered_list['First Name']

    fulfillment['Last Name'] = filtered_list['Last Name']

    fulfillment['Company Name'] = filtered_list['Company Name']

    fulfillment['Fulfillment Type'] = filtered_list['Fulfillment Type']

    fulfillment['Ship City'] = filtered_list['Ship City']

    fulfillment['Install City'] = filtered_list['Install City']

    fulfillment['Ship State'] = filtered_list['Ship State']

    fulfillment['Install State'] = filtered_list['Install State']

    fulfillment['Ship Country'] = filtered_list['Ship Country']

    fulfillment['Install Country'] = filtered_list['Install Country']

    fulfillment['Serial #'] = filtered_list['Serial #']

    fulfillment['Tracking #'] = filtered_list['Tracking #']

    cleaned_df = fulfillment

    return cleaned_df.to_json()

@app.callback(Output('table_ship_asset', 'children'), [Input('intermediate-value_ship_asset', 'children')])
def orders_table(jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)
        return html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='datatable-interactivity_ship_asset',
                        columns=[
                            {"name": 'Status', "id": 'Status'},
                            {"name": 'Created At', "id": 'Created At'},
                            {"name": 'Internal ID', "id": 'Internal ID', "hidden":True},
                            {"name": 'Invoice #', "id": 'Invoice #', "hidden":True},
                            {"name": 'Processing Bank', "id": 'Processing Bank', "hidden":True},
                            {"name": 'Customer Email', "id": 'Customer Email'},
                            {"name": 'Sales Agent', "id": 'Sales Agent'},
                            {"name": 'First Name', "id": 'First Name'},
                            {"name": 'Last Name', "id": 'Last Name'},
                            {"name": 'Company Name', "id": 'Company Name'},
                            {"name": 'Fulfillment Type', "id": 'Fulfillment Type'},
                            {"name": 'Ship City', "id": 'Ship City', "hidden":True},
                            {"name": 'Install City', "id": 'Install City', "hidden":True},
                            {"name": 'Ship State', "id": 'Ship State', "hidden":True},
                            {"name": 'Install State', "id": 'Install State', "hidden":True},
                            {"name": 'Ship Country', "id": 'Ship Country', "hidden":True},
                            {"name": 'Install Country', "id": 'Install Country', "hidden":True},
                            {"name": 'Serial #', "id": 'Serial #', "hidden":True},
                            {"name": 'Tracking #', "id": 'Tracking #', "hidden":True}
                        ],
                        data=fulfillment.to_dict("rows"),
                        editable=False,
                        sort_action=True,
                        sort_mode="single",
                        row_selectable="single",
                        selected_rows=[],
                        style_table={'margin-top': 10, 'overflowX': 'scroll'},
                        style_cell={
                            'font-size': '12px',
                            'text-align': 'center'
                        }
                    ),
                ], className='twelve columns'),
            ])



@app.callback(
    output=Output('display_selected_row_ship_asset', "children"),
    inputs=[Input('datatable-interactivity_ship_asset', "selected_rows")],
    state=[State('intermediate-value_ship_asset', 'children'), State('datatable-interactivity_ship_asset', "data")])
def update_table(selected_rows, jsonified_cleaned_data, rows):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)
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
            dff = fulfillment
        else:
            dff = pd.DataFrame(rows)

        dff = dff.iloc[selected_rows]

        if selected_rows == []:
            return ''
        else:
            return html.Div([
                        html.Div(
                            dash_table.DataTable(
                                id='display_selected_row_data_table_ship_asset',
                                columns=[
                                    {"name": 'Status', "id": 'Status'},
                                    {"name": 'Created At', "id": 'Created At'},
                                    {"name": 'Internal ID', "id": 'Internal ID', "hidden":True},
                                    {"name": 'Invoice #', "id": 'Invoice #', "hidden":True},
                                    {"name": 'Processing Bank', "id": 'Processing Bank', "hidden":True},
                                    {"name": 'Customer Email', "id": 'Customer Email'},
                                    {"name": 'Sales Agent', "id": 'Sales Agent'},
                                    {"name": 'First Name', "id": 'First Name'},
                                    {"name": 'Last Name', "id": 'Last Name'},
                                    {"name": 'Company Name', "id": 'Company Name'},
                                    {"name": 'Fulfillment Type', "id": 'Fulfillment Type'},
                                    {"name": 'Ship City', "id": 'Ship City', "hidden":True},
                                    {"name": 'Install City', "id": 'Install City', "hidden":True},
                                    {"name": 'Ship State', "id": 'Ship State', "hidden":True},
                                    {"name": 'Install State', "id": 'Install State', "hidden":True},
                                    {"name": 'Ship Country', "id": 'Ship Country', "hidden":True},
                                    {"name": 'Install Country', "id": 'Install Country', "hidden":True},
                                    {"name": 'Serial #', "id": 'Serial #', "hidden":True},
                                    {"name": 'Tracking #', "id": 'Tracking #', "hidden":True}
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
                                html.Div(dcc.DatePickerSingle(
                                    id='ship_date_ship_asset',
                                    date=datetime.datetime.today().strftime('%Y-%m-%d'),
                                    display_format='YYYY-MM-DD'
                                    )),
                                html.Button('Submit', id='button_ship_asset'),
                                html.Div(html.H5(id='output-container-button_ship_asset'))
                            ])
                        , className='twelve columns')
                    ])



@app.callback(
    Output('output-container-button_ship_asset', 'children'),
    [Input('button_ship_asset', 'n_clicks')],
    state=[State('ship_date_ship_asset', 'date'), State('datatable-interactivity_ship_asset', "selected_rows"), State('intermediate-value_ship_asset', 'children')])
def update_output(n_clicks, ship_date, row, jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)

        if n_clicks == None:
            return 'Select shipment date and press submit'
        else:
            if ship_date  == '':
                return 'A date is needed.'
            else:
                selected_row = (fulfillment.iloc[[row[0]]].to_dict("rows"))[0]

                if selected_row.get('install_city', '') == '':
                    location_city = selected_row['Ship City']
                else:
                    location_city = selected_row['Install City']

                if selected_row.get('install_state', '') == '':
                    location_state = selected_row['Ship State']
                else:
                    location_state = selected_row['Install State']

                if selected_row.get('install_country', '') == '':
                    country_code = selected_row['Ship Country']
                else:
                    country_code = selected_row['Install Country']

                invoice_id = selected_row.get('Invoice #', ' ')

                internal_id = selected_row.get('Internal ID', ' ')

                created_at = selected_row.get('Created At', ' ')

                sales_agent = selected_row.get('Sales Agent', ' ')

                company_name = selected_row.get('Company Name', ' ')

                customer_first_name = selected_row.get('First Name', ' ')

                customer_last_name = selected_row.get('Last Name', ' ')

                alias = selected_row.get('Customer Email', ' ')

                serial_num = selected_row.get('Serial #', ' ')

                trk_num = selected_row.get('Tracking #', ' ')

                location_name = selected_row['Company Name'].replace('&', ' ').replace('/', '_') + ' - ' + location_city + ' - ' + location_state

                if len(location_name) > 50:
                    too_long = len(location_name) - 50
                    old_location_name = location_name
                    location_name = (company_name.replace('&', ' ').replace('/', ' ')[:-too_long]) + ' - ' + location_city + ' - ' + location_state
                    app.logger.info('Shortened Location/Network Name from: \'' + old_location_name + '\' to: \'' + location_name + '\'')
                else:
                    pass

                app.logger.info('Updating asset in Snipe-IT...')

                update_asset(serial_num, ship_date)

                app.logger.info('Updating row on Google Master Spreadsheet...')

                update_master_gsheet(created_at, sales_agent, ship_date)

                app.logger.info(('The device with the Serial# "{}" has been set to ship to "{}"').format(serial_num, location_name))
                return ('The device with the Serial# "{}" has been set to ship to "{}"').format(serial_num, location_name)
