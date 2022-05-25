import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import requests
import json
import pandas as pd
from gspread_pandas import Spread
import datetime
import gspread_pandas
from main_path import main_path


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501



#This sets the creds to come from the 'google_secret.json' file that is in the repo with the app
creds = gspread_pandas.conf.get_config(conf_dir=f'{main_path}/project_mssapp/', file_name='google_secret.json')



def update_inventory_manager_sheet():
    now = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    #print(now)

    snipe_it_api_key = "snipe_it_api_key"

    url = "https://securitymetricsmss.snipe-it.io/api/v1/hardware"

    querystring = {"limit":"5000","search":""}

    payload = ""

    headers = {
        'Accept': "application/json",
        'Authorization': "Bearer " + snipe_it_api_key
        }

    app.logger.info('requesting data from Snipe-IT')

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    app.logger.debug(response)

    data = json.loads(response.text)['rows']

    #data[0]

    data_clean = {'Model': [],
                  'Serial #': [],
                  'Status': [],
                  'Date Shipped': [],
                  'Processing Bank/Group': [],
                  'Type': [],
                  'Assigned to': [],
                  'Asset Name': [],
                  'Last Updated: ' + now: []}

    inventory = pd.DataFrame(data=data_clean)

    app.logger.info('creating inventory dataframe')

    for row in data:
        try:
            if row['custom_fields'].get('Type', '') == '':
                if row['assigned_to'] is None:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
                else:
                                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Assigned to': row['assigned_to']['name'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
            else:
                if row['assigned_to'] is None:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Type': row['custom_fields']['Type']['value'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
                else:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Type': row['custom_fields']['Type']['value'],
                                                  'Assigned to': row['assigned_to']['name'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)

        except:
            app.logger.exception(row)
            pass

    a = 500
    while len(data) == 500:
        querystring = {"limit":"500","offset":a}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        data = response.json()['rows']

        for row in data:
            if row['custom_fields'].get('Type', '') == '':
                if row['assigned_to'] is None:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
                else:
                                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Assigned to': row['assigned_to']['name'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
            else:
                if row['assigned_to'] is None:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Type': row['custom_fields']['Type']['value'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)
                else:
                    inventory = inventory.append({'Model': row['model']['name'],
                                                  'Serial #': row['serial'],
                                                  'Status': row['status_label']['name'] + '(' + row['status_label']['status_meta'] + ')',
                                                  'Date Shipped': row['custom_fields']['Date Shipped']['value'],
                                                  'Processing Bank/Group': row['custom_fields']['Processing Bank']['value'],
                                                  'Type': row['custom_fields']['Type']['value'],
                                                  'Assigned to': row['assigned_to']['name'],
                                                  'Asset Name': row['name'],
                                                 }, ignore_index=True)

        a += 500
        print('group done')

    #inventory

    app.logger.info('gathering spreadsheet data')

    #This sets the spreadsheet that the code will be working with.
    s = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)

    app.logger.debug(s)

    app.logger.debug(s.sheets)

    #This sets the worksheet in the spreadsheet that the code will be working with.
    data_sheet = 'Name of worksheet'

    app.logger.debug(s.url)

    #This opens the worksheet that was selected.
    s.open_sheet(data_sheet)
    #s

    app.logger.info('sending data to spreadsheet')

    #Send data back to googlesheet
    s.df_to_sheet(inventory, sheet=data_sheet, start='A1', replace=True, index=False)


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", "time_saved":"5", "note":"Manual MSS App updating Snipe-IT inventory in inventory manager spreadsheet"}'

    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)


    app.logger.debug('Time saved for fulfillment (in minutes) - 5')

    return 200










layout = html.Div([
    html.Div([
        html.H2('Update Inventory Manager Spreadsheet'),
        html.P('This will be used to update the \'Inventory Manager\' with the current inventory information from the Snipe-IT database.', style={'fontSize':14})
    ], className='ten columns offset-by-one', style={'margin-top': 10}),
   html.Div([
       html.Button('Submit', id='button-2_update_inventory_manager_sheet'),
   ], className='ten columns offset-by-one', style={'margin-top': 30}),
   html.Div([
       html.Div(id='output_update_inventory_manager_sheet')
   ], className='ten columns offset-by-one', style={'margin-top': 10})
])










@app.callback(
    Output('output_update_inventory_manager_sheet', 'children'),
    [Input('button-2_update_inventory_manager_sheet', 'n_clicks')],
)
def update(n_clicks):
    if n_clicks == None:
        return 'Click Submit to update the work sheet in the spread sheet.'
    elif n_clicks == 1:
        update_inventory_manager_sheet()
        return 'The inventory has been updated on the work sheet in the spread sheet. If you would like to update the inventory again, refresh the page.'
    else:
        return 'The inventory was already updated. Refresh the page if you would like to update the inventory again.'
