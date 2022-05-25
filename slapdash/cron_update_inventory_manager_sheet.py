import requests
import json
import pandas as pd
from gspread_pandas import Spread
import datetime
import gspread_pandas
from main_path import main_path





#######################################################
#This section is what is needed for the logging setup.
#######################################################
import logging
import logging.handlers
import os
from pathlib import Path
import datetime


#This gets the datestamp in the format: 'YYYY_MM_DD'
today = '{0:%Y_%m_%d}'.format(datetime.datetime.now())

#This checks if the logs folder already exists in the diretory.
#The number of '../' needs to bring it outside of the GitHub repository.
#If the folder already exists, continues on.
#If the folder does not already exist, it will create that folder then move on.
my_folder = Path(f"{main_path}/logs/")
if my_folder.is_dir():
    print('Folder already exists')
else:
    os.system(f'mkdir {main_path}/logs/')
    print('Folder Created')

#This sets up the basic logging operation.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s, cron_update_inventory_manager_sheet, %(levelname)s, %(message)s',
                              "%Y-%m-%d %H:%M:%S")

#This sets up the logging that will be sent to the file for the current date.
file_handler = logging.handlers.TimedRotatingFileHandler(f'{main_path}/logs/cron_update_inventory_manager_sheet.log', when="midnight")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

#This sets up the logging that will be displayed on the terminal screen.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

#This activates each of the handliers in the program.
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

#######################################################
#######################################################





#This sets the creds to come from the 'google_secret.json' file that is in the repo with the app
creds = gspread_pandas.conf.get_config(conf_dir=f'{main_path}/project_mssapp/', file_name='google_secret.json')

def update_inventory_manager_sheet():
    now = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    #print(now)

    snipe_it_api_key = "snipe_it_api_key"

    url = "https://company.snipe-it.io/api/v1/hardware"

    querystring = {"limit":"10000"}

    payload = ""

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipe_it_api_key
    }

    attempt = 1

    logger.info('requesting data from Snipe-IT, attempt: ' + str(attempt))

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    logger.debug('response.text - ' + str(response))

    logger.info('response.status_code - ' + str(response.status_code))

    logger.debug('response.headers - ' + str(response.headers))

    logger.debug('response.history - ' + str(response.history))

    logger.debug('response.url - ' + str(response.url))

    while str(response.status_code) == '500':
        attempt += 1

        logger.info('requesting data from Snipe-IT attempt: ' + str(attempt))

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        logger.debug('response.text - ' + str(response))

        logger.info('response.status_code - ' + str(response.status_code))

        logger.debug('response.headers - ' + str(response.headers))

        logger.debug('response.history - ' + str(response.history))

        logger.debug('response.url - ' + str(response.url))


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

    logger.info('creating inventory dataframe')

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
            logger.exception(row)
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
        logger.debug('group done')

    #inventory

    logger.info('gathering spreadsheet data')

    #gc = authenticate_google_docs()
    #for s in gc.openall():
    #     print s.title

    #This sets the spreadsheet that the code will be working with.
    s = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)

    logger.debug(s)

    logger.debug(s.sheets)

    #This sets the worksheet in the spreadsheet that the code will be working with.
    data_sheet = 'Name of worksheet'

    logger.debug(s.url)

    #This opens the worksheet that was selected.
    s.open_sheet(data_sheet)
    #s

    logger.info('sending data to spreadsheet')

    #Send data back to googlesheet
    s.df_to_sheet(inventory, sheet=data_sheet, start='A1', replace=True, index=False)


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", "time_saved":"0.2083", "note":"Auto Cron - updating Snipe-IT inventory in inventory manager spreadsheet"}'

    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)


    logger.info('Time saved for fulfillment (in minutes) - 0.2083')

    return 200


update_inventory_manager_sheet()
