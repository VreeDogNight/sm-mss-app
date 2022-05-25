import requests
from gspread_pandas import Spread
import gspread_pandas
import pandas as pd
import datetime
import time
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

formatter = logging.Formatter('%(asctime)s, cron_check_future_sales_orders, %(levelname)s, %(message)s',
                              "%Y-%m-%d %H:%M:%S")

#This sets up the logging that will be sent to the file for the current date.
file_handler = logging.handlers.TimedRotatingFileHandler(f'{main_path}/logs/cron_check_future_sales_orders.log', when="midnight")
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





logger.debug('######################### NEW PROCESS #########################')

today_order = datetime.datetime.today().strftime('%Y-%m-%d')

#This sets the creds to come from the 'google_secret.json' file that is in the repo with the app
creds = gspread_pandas.conf.get_config(conf_dir=f'{main_path}/project_mssapp/', file_name='google_secret.json')

#This sets the spreadsheet that the code will be working with.
s = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)
#s

#s.sheets

#This sets the worksheet in the spreadsheet that the code will be working with.
data_sheet = 'Name of worksheet'

#s.url

#This opens the worksheet that was selected.
s.open_sheet(data_sheet)
#s

#This converts the contents of the worksheet to be a pandas DataFrame so that the information can be manipulated.
df = s.sheet_to_df(header_rows=1,index=False).astype(str)

#df

for index, order in df.iterrows():
    if order['Fulfillment Date'] <= today_order:
        if order['Invoice #'] != '':
            if order['Fulfilled'] != 'Done':
                order['Fulfilled'] = 'Done'

                row_number = str(order.name + 2)

                logger.debug('row_number: ' + row_number)
                logger.debug('created_at: ' + order['Created At'])

                s.update_cells(start=(str('A' + row_number)), end=(str('Y' + row_number)), vals=order)

                data = {
                  'name_first': order['First Name'],
                  'sales_agent': order['Sales Agent'],
                  'install_state': order['Install State'],
                  'install_address': order['Install Address'],
                  'country_code': order['Ship Country'],
                  'location_city': order['Ship City'],
                  'install_zip': order['Install Zip'],
                  'install_city': order['Install City'],
                  'loc_zip': order['Ship Zip'],
                  'customer_id': order['Internal ID'],
                  'company_name': order['Company Name'],
                  'phone_number': order['Phone Number'],
                  'fulfillment_type': order['Fulfillment Type'],
                  'processor_bank': order['Processing Bank'],
                  'install_country_code': order['Install Country'],
                  'sales_type': order['Sale Type'],
                  'location_state': order['Ship State'],
                  'name_last': order['Last Name'],
                  'invoice_id': order['Invoice #'],
                  'created_at': today_order,
                  'alias': order['Customer Email'],
                  'location_address': order['Ship Address']
                }

                response = requests.post('https://hooks.zapier.com/hooks/catch/', data=data)
                logger.debug('Zapier Response: ' + response.text)
                time.sleep(1)

        else:
            logger.debug('No Invoice #. created_at: ' + order['Created At'])
