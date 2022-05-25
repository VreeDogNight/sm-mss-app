import requests
import pandas as pd
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

formatter = logging.Formatter('%(asctime)s, cron_get_meraki_network_list, %(levelname)s, %(message)s',
                              "%Y-%m-%d %H:%M:%S")

#This sets up the logging that will be sent to the file for the current date.
file_handler = logging.handlers.TimedRotatingFileHandler(f'{main_path}/logs/cron_get_meraki_network_list.log', when="midnight")
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





def list_all_networks_in_all_orgs(api_key):
    logger.info('Gathering list of all networks.')

    url_org = "https://api.meraki.com/api/v1/organizations"

    payload = ""

    headers = {'X-Cisco-Meraki-API-Key': api_key}

    response_org = requests.request("GET", url_org, data=payload, headers=headers)

    while response_org.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki get orgs Attempt: {attempt}')
        time.sleep(2)
        response_org = requests.request("GET", url_org, data=payload, headers=headers)
        attempt += 1

    data_org = response_org.json()

    logger.info('list_all_networks_in_all_orgs() - ' + str(response_org))

    orgs_list = []

    for org in data_org:
        orgs_list.append(org['id'])

    network_list = []

    logger.info('Putting all networks from all organizations into 1 DataFrame')

    for org in orgs_list:
        url_network = "https://api.meraki.com/api/v1/organizations/" + str(org) + "/networks"
        response_network = requests.request("GET", url_network, data=payload, headers=headers)
        while response_network.status_code == 429:
            attempt = 2
            app.logger.debug(f'Meraki get networks Attempt: {attempt}')
            time.sleep(2)
            response_network = requests.request("GET", url_network, data=payload, headers=headers)
            attempt += 1
        data_network = response_network.json()
        network_list.append(data_network)
        time.sleep(1)

    logger.debug('list_all_networks_in_all_orgs() - ' + str(type(network_list)))

    combined_network_list = []

    for sublist in network_list:
        for item in sublist:
            combined_network_list.append(item)

    logger.debug('list_all_networks_in_all_orgs() - ' + str(type(combined_network_list)))

    try:
        for network in combined_network_list:
            for org in data_org:
                if str(network['organizationId']) == str(org['id']):
                    org_name = org['name']
                    network['organization'] = org_name

        logger.debug('list_all_networks_in_all_orgs() - ' + str(type(combined_network_list)))

        network_df = pd.DataFrame(combined_network_list)

        logger.info('filtering DF to only include networkName and networkId')

        final_network_df = pd.DataFrame()

        final_network_df['name'] = network_df['name']

        final_network_df['id'] = network_df['id']

        return final_network_df

    except:
        logger.exception('Network: ' + str(network) + ' - Network Type: ' + str(type(network)) + ' - Org: ' + str(org) + ' - Org Type: ' + str(type(org)))
        return ''


meraki_networks = list_all_networks_in_all_orgs('meraki_api_key')

logger.info('saving to csv...')

meraki_networks.to_csv(f'{main_path}/project_mssapp/slapdash/current_meraki_networks.csv', index=False)
