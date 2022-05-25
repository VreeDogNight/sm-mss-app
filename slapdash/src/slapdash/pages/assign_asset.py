import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from gspread_pandas import Spread
import dash_table
import requests
import json
import datetime
import gspread_pandas
import time
from main_path import main_path


from ..app import app


app.css.append_css({'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/drNmGx.css'})  # noqa: E501



#This sets the creds to come from the 'google_secret.json' file that is in the repo with the app
creds = gspread_pandas.conf.get_config(conf_dir=f'{main_path}/project_mssapp/', file_name='google_secret.json')



def check_out_asset(serial_num, trk_num, invoice_id, internal_id, location_name):

    app.logger.info('searching for asset ID in Snipe-IT by serial number')

    url = "https://company.snipe-it.io/api/v1/hardware/"

    payload = ""

    snipeit_api_key = 'snipeit_api_key'

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipeit_api_key
    }

    app.logger.debug('Searial #: "' + serial_num + '"')

    response_asset_by_serial = requests.request("GET", url + "byserial/" + serial_num, data=payload, headers=headers)

    asset_search_data = json.loads(response_asset_by_serial.text)

    app.logger.debug('Asset search response Data: "' + response_asset_by_serial.text + '"')

    asset_id = str(asset_search_data['rows'][0]['id'])

    app.logger.debug('Asset ID: "' + asset_id + '"')

    note = 'TRK # ' + trk_num + '\nInvoice ID ' + str(invoice_id)

    app.logger.debug('Note: "' + note + '"')

    name = 'internal_id_' + str(internal_id)

    app.logger.debug('Asset Name: "' + name + '"')

    app.logger.info('searching for location ID in Snipe-IT')

    url_location = "https://company.snipe-it.io/api/v1/locations"

    headers_location = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipeit_api_key
    }

    app.logger.debug('Location Name being searched for: "' + location_name + '"')

    params_location = (
        ('search', location_name),
    )

    response_location = requests.request("GET", url_location, headers=headers_location, params=params_location)

    location_search_data = json.loads(response_location.text)

    if response_location.json()['total'] == 0:
        return 'error'

    else:
        app.logger.debug('Location search response Data: ' + response_location.text)

        location_id = location_search_data['rows'][0]['id']

        app.logger.debug('Location ID: "' + str(location_id) + '"')

        app.logger.info('checking out asset to location in Snipe-IT')

        # Set your server info
        url_checkout = url + asset_id + '/checkout'

        # Create the headers with your auth token
        headers_checkout = {
            'Content-Type': "application/json",
            'Accept': 'application/json',
            'Authorization': "Bearer " + snipeit_api_key
        }

        # Create a payload with the required fields
        payload_checkout = {'assigned_location': location_id, 'checkout_to_type': 'location', 'note': note, 'name': name}

        # Send the request and grab the response as a variable
        response_checkout = requests.post(url_checkout, headers=headers_checkout, json=payload_checkout)

        app.logger.debug('Asset checkout response Data: ' + response_checkout.text)

        asset_checkout_data = json.loads(response_checkout.text)

        app.logger.info(('The Asset: "{}" has been checked out to the Location: "{}", and was assigned the Internal ID # of "{}".').format(
            serial_num, location_name, internal_id
        ))


        date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        headers_record_stats = {'Content-type': 'application/json',}

        data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", "time_saved":"1", "note":"MSS App checking out asset in Snipe-IT"}'

        response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)


        app.logger.debug('Time saved for fulfillment (in minutes) - 1')

        return 'The Asset: "{}" has been checked out to the Location: "{}", and was assigned the Internal ID # of "{}".'.format(
            serial_num, location_name, internal_id
        )



def update_asset(asset_serial, internal_id, invoice_id, trk_num, processing_bank):

    app.logger.info('searching for asset by serial number in Snipe-IT')

    url = "https://company.snipe-it.io/api/v1/hardware/"

    snipeit_api_key = 'snipeit_api_key'

    payload_search = ""

    headers_search = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipeit_api_key
    }

    response_asset_by_serial = requests.request("GET", url + "byserial/" + asset_serial, data=payload_search, headers=headers_search)

    app.logger.debug('Asset search response Data: ' + response_asset_by_serial.text)

    asset_search_data = json.loads(response_asset_by_serial.text)

    asset_id = str(asset_search_data['rows'][0]['id'])

    app.logger.debug('Asset ID: "' + asset_id + '"')

    app.logger.info('updating asset in Snipe-IT')

    url_update = url + asset_id

    app.logger.debug('Internal ID: "' + str(internal_id) + '"')

    app.logger.debug('Invoice ID: "' + str(invoice_id) + '"')

    app.logger.debug('Tracking #: "' + str(trk_num) + '"')

    app.logger.debug('Processing Bank: "' + str(processing_bank) + '"')

    payload_update = 'name=internal_id_' + str(internal_id) + '&_snipeit_invoice_id_3=' + str(invoice_id) + '&_snipeit_tracking_5=' + trk_num + '&undefined=&_snipeit_processing_bank_18=' + processing_bank + '&_snipeit_internal_id_19=' + str(internal_id)

    headers_update = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + snipeit_api_key
        }

    response_update = requests.request("PUT", url_update, data=payload_update, headers=headers_update)

    app.logger.debug('Asset update response Data: ' + response_update.text)

    asset_update_data = json.loads(response_update.text)

    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", "time_saved":"1", "note":"MSS App updating details on the asset in Snipe-IT"}'

    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)

    app.logger.debug('Time saved for fulfillment (in minutes) - 1')

    return response_update.text



def claim_device_add_tags_meraki_network(serial_num, network_name, company_name, country_code, customer_first_name, customer_last_name, alias, customer_id, location_city, location_state, location_address, location_zip, partner_code):

    s = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)

    app.logger.debug(s)

    app.logger.debug(s.sheets)

    data_sheet = 'Name of worksheet'

    app.logger.debug(s.url)

    s.open_sheet(data_sheet)
    #s

    df_test = s.sheet_to_df(header_rows=1).astype(str)
    #df_test

    app.logger.debug('Network Name: "' + network_name + '"')
    for index, row in df_test.iterrows():
        if (row['Location Name']).replace('&', ' ') == network_name:
            network_id = row['Meraki_Net_Id']
            vpn_subnet = row['VPN NAT IP']

    url_claim = "https://api.meraki.com/api/v1/networks/" + network_id + "/devices/claim"

    payload_claim = "{\"serials\":[\"" + serial_num + "\"]}"

    app.logger.debug('Serial #: "' + str(serial_num) + '"')

    headers_claim = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_claim = requests.request("POST", url_claim, data=payload_claim, headers=headers_claim)

    while response_claim.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki Claim Device Attempt: {attempt}')
        time.sleep(2)
        response_claim = requests.request("POST", url_claim, data=payload_claim, headers=headers_claim)
        attempt += 1

    app.logger.debug('response_claim: ' + str(response_claim.text))

    url_tags = "https://api.meraki.com/api/v1/devices/" + serial_num

    app.logger.debug('Company Name: "' + str(company_name) + '"')

    app.logger.debug('Customer First Name: "' + str(customer_first_name) + '"')

    app.logger.debug('Customer Last Name: "' + str(customer_last_name) + '"')

    app.logger.debug('Email: "' + str(alias) + '"')

    app.logger.debug('Customer ID: "' + str(customer_id) + '"')

    app.logger.debug('Street Address: "' + str(location_address) + '"')

    app.logger.debug('City: "' + str(location_city) + '"')

    app.logger.debug('State: "' + str(location_state) + '"')

    app.logger.debug('Postal Code: "' + str(location_zip) + '"')

    app.logger.debug('Country Code: "' + str(country_code) + '"')

    network_tags = '"' + company_name.replace(' ', '_') + '", "' + country_code.replace(' ', '_') + '", "' + customer_first_name.replace(' ', '_') + '_' + customer_last_name.replace(' ', '_') + '", "' + alias.replace(' ', '_') + '", "' + ('customer_id_' + str(customer_id)).replace(' ', '_') + '", "' + (location_city).replace(' ', '_') + '", "' + location_state.replace(' ', '_') + '", "Pod_1", "Hub_1"'

    address = location_address + ' ' + location_city + ' ' + location_state + ' ' + str(location_zip)

    payload_tags = "{\"name\":\"" + network_name + "\", \"tags\":[" + network_tags + "], \"address\":\"" + address + "\", \"moveMapMarker\": true}"
    #payload_tags

    headers_tags = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_tags = requests.request("PUT", url_tags, data=payload_tags, headers=headers_tags)

    while response_tags.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki add tags Attempt: "{attempt}"')
        time.sleep(2)
        response_tags = requests.request("PUT", url_tags, data=payload_tags, headers=headers_tags)
        attempt += 1



    url_site_to_site = "https://api.meraki.com/api/v1/networks/" + network_id + "/appliance/vpn/siteToSiteVpn"
    #url_site_to_site

    payload_site_to_site = "{\"mode\": \"spoke\",\"hubs\": [{\"hubId\": \"N_1234567890\",\"useDefaultRoute\": false}]}"
    #payload_site_to_site

    headers_site_to_site = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }
    #headers_site_to_site

    time.sleep(1)

    response_site_to_site = requests.request("PUT", url_site_to_site, data=payload_site_to_site, headers=headers_site_to_site)

    while response_site_to_site.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki site to site setup Attempt: "{attempt}"')
        time.sleep(2)
        response_site_to_site = requests.request("PUT", url_site_to_site, data=payload_site_to_site, headers=headers_site_to_site)
        attempt += 1

    app.logger.debug(f'Site to site data: {response_site_to_site}')

    data_site_to_site = response_site_to_site.json()

    url_network_vlans = "https://api.meraki.com/api/v1/networks/" + network_id + "/appliance/vlans"
    #url_network_vlans

    headers_network_vlans = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_network_vlans = requests.request("GET", url_network_vlans, headers=headers_network_vlans)

    app.logger.debug(response_network_vlans)

    data_network_vlans = response_network_vlans.json()

    vlan_id = 'vlan not found'
    for vlan in data_network_vlans:
        if vlan['name'] == 'CDE':
            vlan_id = str(vlan['id'])

    app.logger.debug('"' + vlan_id + '"')

    url_vpn_subnet = "https://api.meraki.com/api/v1/networks/" + network_id + "/appliance/vlans/" + vlan_id
    #url_vpn_subnet

    payload_vpn_subnet = "{\"vpnNatSubnet\": \"" + vpn_subnet + "\"}"
    #payload_vpn_subnet

    headers_vpn_subnet = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_vpn_subnet = requests.request("PUT", url_vpn_subnet, data=payload_vpn_subnet, headers=headers_vpn_subnet)

    while response_vpn_subnet.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki vpn subnet  setup Attempt: "{attempt}"')
        time.sleep(2)
        response_vpn_subnet = requests.request("PUT", url_vpn_subnet, data=payload_vpn_subnet, headers=headers_vpn_subnet)
        attempt += 1

    data_vpn_subnet = response_vpn_subnet.json()

    app.logger.debug('"' + data_vpn_subnet + '"')

    payload = '{"name": "name","timeZone": "time","tags": "tag","type": "appliance wireless","copyFromNetworkId": "N_678917643826109453"}'


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Firewall Technician", "time_saved":"XX", "note":"MSS App assigning Meraki device to network and updating the device in Meraki system"}'

#    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/3803642/vbdkth/', headers=headers_record_stats, data=data_record_stats)

#    app.logger.debug('Time saved for firewall tech (in minutes) - XX')

    return network_id



def update_master_gsheet(created_at, sales_agent, trk_num, serial_num, fulfillment_type):
    time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    #This sets the spreadsheet that the code will be working with.
    s_start = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)
    #s_start

    #s_start.sheets

    #This sets the worksheet in the spreadsheet that the code will be working with.
    data_sheet_start = 'Name of worksheet'

    #s_start.url

    #This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)
    #s_start

    #This converts the contents of the worksheet to be a pandas DataFrame so that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    #df_start

    for index, row in df_start.iterrows():
        if row['Created At'] == created_at:
            if row['Sales Agent'] == sales_agent:
                if row['Fulfillment Type'] == fulfillment_type:
                    row_number = str(row.name + 2)
                    new_row_data = [
                        'Assigned',
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
                        serial_num,
                        trk_num,
                        row['Not Checked'],
                        row['Checked'],
                        time_stamp,
                        row['Shipped'],
                        row['Delivered'],
                        row['Online'],
                        row['Notes'],
                        row['Sale Type'],
                    ]
                    s_start.update_cells(start=(str('A' + row_number)), end=(str('AJ' + row_number)), vals=new_row_data)
        else:
            pass

    return ''



def setup_internal_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid, serial_number, collector_type, collector_identifier, enable_syslog_tracking):
    OAUTH_CLIENT_ID = 'OAUTH_CLIENT_ID'
    OAUTH_CLIENT_SECRET = 'OAUTH_CLIENT_SECRET'
    class mss_auth:
        def authenticate(self):
            """
            Get a Bearer Token for the OAuth Client.

            I make a request to /smauth/token to get a bearer token

            Raises:
                requests.HTTPError

            """
            response = requests.post(
                'url to request token',
                auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
                headers={'content-type': 'application/x-www-form-urlencoded'},
                data='grant_type=client_credentials')
            response.raise_for_status()
            token_data = response.json()
            return token_data.get('access_token')

        def check_token_validity(self, token):
            """
            Check if the access token is still valid.

            Args:
                token (str): the access token

            Returns:
                bool: validity of access_token

            """
            response = requests.get('url to check token validity', headers={'Authorization': 'Bearer {0}'.format(token)})
            if response.ok:
                return response.json().get('status', False)
            return False

    aa = mss_auth()
    token = str(aa.authenticate())
    app.logger.debug('SM Token: ' + token)
    app.logger.debug('SM Token Check: ' + str(aa.check_token_validity(token)))

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token,
        'Connection': 'keep-alive',
    }

    #print('Headers: ' + headers)

    location_full_address = (location_address + ' ' + location_city + ' ' + location_state + ' ' + str(location_zip)).replace(',','').replace('\n','')

    data_location_creation = '{"location_data": {"name": "' + location_name + '", "address": "' + location_full_address + '"}}'
    app.logger.debug('data_location_creation: ' + data_location_creation)

    app.logger.info('Creating Pulse Location')
    response_location_creation = requests.post('url for internal tool api' + org_uuid + '/locations', headers=headers, data=data_location_creation).json()

    app.logger.debug('response_location_creation: ' + str(response_location_creation))

    response_search_location = requests.get('url for internal tool api' + org_uuid + '/locations', headers=headers).json()

    data_search_location = response_search_location['entries']

    for location in data_search_location:
        if location['name'] == location_name:
            location_uuid = location['cached_data']['location_uuid']

    app.logger.debug('Location uuid: "' + location_uuid + '"')


    data_sensor_name_shell = (
        '{"kind":"internal","name":"' + serial_number + '"}'
    )

    app.logger.info('Creating Pulse Sensor Name Shell')
    response_sensor_name_shell = requests.post('url for internal tool api', headers=headers, data=data_sensor_name_shell).json()
    app.logger.debug('response_sensor_name_shell create: ' + str(response_sensor_name_shell))

    params_search_sensor_shell = (
        ('search', serial_number),
    )

    response_search_sensor_shell = requests.get('url for internal tool api', headers=headers, params=params_search_sensor_shell).json()
    app.logger.debug('response_search_sensor_shell search: ' + str(response_search_sensor_shell))

    data_search_sensor_shell = response_search_sensor_shell['entries']

    for sensor in data_search_sensor_shell:
        if sensor['name'] == serial_number:
            sensor_uuid = sensor['uuid']

    app.logger.debug('Sensor uuid: "' + sensor_uuid + '"')


    app.logger.info('Assigning Device to Sensor')
    app.logger.debug('collector_identifier: "' + collector_identifier + '"')
    data_assign_device = '{"collector_type":"' + collector_type + '","collector_identifier":"' + collector_identifier + '"}'

    response_assign_device = requests.post('url for internal tool api' + sensor_uuid + '/data_collector', headers=headers, data=data_assign_device)
    app.logger.debug('response_assign_device: ' + str(response_assign_device))

    app.logger.info('Assigning Sensor to Location')
    data_assign_sensor = '{"sensor_uuid":"' + sensor_uuid + '"}'

    response_assign_sensor = requests.post('url for internal tool api' + location_uuid + '/sensors', headers=headers, data=data_assign_sensor)
    app.logger.debug('response_assign_sensor: ' + str(response_assign_sensor))


    if enable_syslog_tracking == 'True':
        app.logger.info('Enabling Syslog Tracking')
        data_enable_syslog_tracking = '{"data_type_uuid":"data_type_uuid"}'

        response_enable_syslog_tracking = requests.post('url for internal tool api' + sensor_uuid + '/data_types', headers=headers, data=data_enable_syslog_tracking)


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json'}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Firewall Technician", "time_saved":"XX", "note":"MSS App creating Pulse Location, creating Pulse Sensor, assigning device to Pulse Sensor, assigning Pulse Sensor to Pulse Location, and if necessary enable syslog tracking in Pulse."}'

#    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)

#    app.logger.debug('Time saved for firewall tech (in minutes) - XX')

    return ''



def setup_external_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid):
    OAUTH_CLIENT_ID = 'OAUTH_CLIENT_ID'
    OAUTH_CLIENT_SECRET = 'OAUTH_CLIENT_SECRET'
    class mss_auth:
        def authenticate(self):
            """
            Get a Bearer Token for the OAuth Client.

            I make a request to /smauth/token to get a bearer token

            Raises:
                requests.HTTPError

            """
            response = requests.post(
                'url to request token',
                auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
                headers={'content-type': 'application/x-www-form-urlencoded'},
                data='grant_type=client_credentials')
            response.raise_for_status()
            token_data = response.json()
            return token_data.get('access_token')

        def check_token_validity(self, token):
            """
            Check if the access token is still valid.

            Args:
                token (str): the access token

            Returns:
                bool: validity of access_token

            """
            response = requests.get('url to check token validity', headers={'Authorization': 'Bearer {0}'.format(token)})
            if response.ok:
                return response.json().get('status', False)
            return False

    aa = mss_auth()
    token = str(aa.authenticate())
    app.logger.debug('SM Token: ' + token)
    app.logger.debug('SM Token Check: ' + str(aa.check_token_validity(token)))

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token,
        'Connection': 'keep-alive',
    }

    #print('Headers: ' + headers)

    location_full_address = (location_address + ' ' + location_city + ' ' + location_state + ' ' + str(location_zip)).replace(',','').replace('\n','')

    response_search_location = requests.get('url for internal tool api' + org_uuid + '/locations', headers=headers).json()

    data_search_location = response_search_location['entries']

    for location in data_search_location:
        if location['name'] == location_name:
            location_uuid = location['cached_data']['location_uuid']

    app.logger.debug('Location uuid: "' + location_uuid + '"')


    data_sensor_name_shell = (
        '{"kind":"external","name":"' + location_name + ' External Sensor"}'
    )

    app.logger.info('Creating Pulse Sensor Name Shell')
    response_sensor_name_shell = requests.post('url for internal tool api', headers=headers, data=data_sensor_name_shell).json()
    app.logger.debug('response_sensor_name_shell create: ' + str(response_sensor_name_shell))

    params_search_sensor_shell = (
        ('search', location_name + ' External Sensor'),
    )

    response_search_sensor_shell = requests.get('url for internal tool api', headers=headers, params=params_search_sensor_shell).json()
    app.logger.debug('response_search_sensor_shell search: ' + str(response_search_sensor_shell))

    data_search_sensor_shell = response_search_sensor_shell['entries']

    for sensor in data_search_sensor_shell:
        if sensor['name'] == location_name + ' External Sensor':
            sensor_uuid = sensor['uuid']

    app.logger.debug('Sensor uuid: "' + sensor_uuid + '"')

    app.logger.info('Assigning Sensor to Location')
    data_assign_sensor = '{"sensor_uuid":"' + sensor_uuid + '"}'

    response_assign_sensor = requests.post('url for internal tool api' + location_uuid + '/sensors', headers=headers, data=data_assign_sensor)
    app.logger.debug('response_assign_sensor: ' + str(response_assign_sensor))

    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    headers_record_stats = {'Content-type': 'application/json'}

    data_record_stats = '{"date_time":"' + date_time_record_stats + '", "group":"Firewall Technician", "time_saved":"XX", "note":"MSS App creating Location, creating Sensor, assigning device to Sensor, assigning Sensor to Location, and if necessary enable syslog tracking."}'

#    response_record_stats = requests.post('https://hooks.zapier.com/hooks/catch/', headers=headers_record_stats, data=data_record_stats)

#    app.logger.debug('Time saved for firewall tech (in minutes) - XX')

    return ''



def find_emvee_collector_identifier(serial_number):
    OAUTH_CLIENT_ID = 'OAUTH_CLIENT_ID'
    OAUTH_CLIENT_SECRET = 'OAUTH_CLIENT_SECRET'
    class mss_auth:
        def authenticate(self):
            """
            Get a Bearer Token for the OAuth Client.

            I make a request to /smauth/token to get a bearer token

            Raises:
                requests.HTTPError

            """
            response = requests.post(
                'url to request token',
                auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
                headers={'content-type': 'application/x-www-form-urlencoded'},
                data='grant_type=client_credentials')
            response.raise_for_status()
            token_data = response.json()
            return token_data.get('access_token')

        def check_token_validity(self, token):
            """
            Check if the access token is still valid.

            Args:
                token (str): the access token

            Returns:
                bool: validity of access_token

            """
            response = requests.get('url to check token validity', headers={'Authorization': 'Bearer {0}'.format(token)})
            if response.ok:
                return response.json().get('status', False)
            return False

    aa = mss_auth()
    token = str(aa.authenticate())
    app.logger.debug('SM Token: ' + token)
    app.logger.debug('SM Token Check: ' + str(aa.check_token_validity(token)))

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token,
        'Connection': 'keep-alive',
    }

    #print('Headers: ' + headers)

    params = (
        ('items_per_page', '10000'),
        ('unused', 't'),
    )

    app.logger.debug('Searching for emvee uuid...')

    response = requests.get(f'url for internal tool api/{serial_number}', headers=headers)

    app.logger.debug(f'Search Response: {response.text}')

    data = response.json()

    device_uuid = data['uuid']

    return device_uuid



def create_new_pulse_org(organization_name):
    OAUTH_CLIENT_ID = 'OAUTH_CLIENT_ID'
    OAUTH_CLIENT_SECRET = 'OAUTH_CLIENT_SECRET'
    class mss_auth:
        def authenticate(self):
            """
            Get a Bearer Token for the OAuth Client.

            I make a request to /smauth/token to get a bearer token

            Raises:
                requests.HTTPError

            """
            response = requests.post(
                'url to request token',
                auth=(OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET),
                headers={'content-type': 'application/x-www-form-urlencoded'},
                data='grant_type=client_credentials')
            response.raise_for_status()
            token_data = response.json()
            return token_data.get('access_token')

        def check_token_validity(self, token):
            """
            Check if the access token is still valid.

            Args:
                token (str): the access token

            Returns:
                bool: validity of access_token

            """
            response = requests.get('url to check token validity', headers={'Authorization': 'Bearer {0}'.format(token)})
            if response.ok:
                return response.json().get('status', False)
            return False

    aa = mss_auth()
    token = str(aa.authenticate())
    app.logger.debug('SM Token: ' + token)
    app.logger.debug('SM Token Check: ' + str(aa.check_token_validity(token)))

    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'application/json',
        'Authorization': 'Bearer '+token,
        'Connection': 'keep-alive',
    }

    #print('Headers: ' + headers)


    app.logger.debug('Creating new organization...')

    data = {"name": organization_name}

    app.logger.debug('org name: "' + organization_name + '"')

    response = requests.post('url for internal tool api', headers=headers, data=json.dumps(data))

    app.logger.debug('org creation text response:' + response.text)

    response_data = response.json()

    org_uuid = response_data['uuid']

    return org_uuid



def meraki_claim_tag_wireless_access_point(serial_num, network_name, company_name, country_code, customer_first_name, customer_last_name, alias, customer_id, location_city, location_state, location_address, location_zip, partner_code):

    s = Spread('Name of Credentials', 'Name Of Google Spreadsheet', config=creds)

    app.logger.debug(s)

    app.logger.debug(s.sheets)

    data_sheet = 'Name of worksheet'

    app.logger.debug(s.url)

    s.open_sheet(data_sheet)
    #s

    df_test = s.sheet_to_df(header_rows=1).astype(str)
    #df_test

    app.logger.debug('Network Name: "' + network_name + '"')
    for index, row in df_test.iterrows():
        if (row['Location Name']).replace('&', ' ') == network_name:
            network_id = row['Meraki_Net_Id']
            vpn_subnet = row['VPN NAT IP']

    url_claim = "https://api.meraki.com/api/v1/networks/" + network_id + "/devices/claim"

    payload_claim = "{\"serials\":[\"" + serial_num + "\"]}"

    app.logger.debug('Serial #: "' + str(serial_num) + '"')

    headers_claim = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_claim = requests.request("POST", url_claim, data=payload_claim, headers=headers_claim)

    while response_claim.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki claim WAP Attempt: "{attempt}"')
        time.sleep(2)
        response_claim = requests.request("POST", url_claim, data=payload_claim, headers=headers_claim)
        attempt += 1

    app.logger.debug('response_claim: ' + str(response_claim.text))

    url_tags = "https://api.meraki.com/api/v1/devices/" + serial_num

    app.logger.debug('Company Name: "' + str(company_name) + '"')

    app.logger.debug('Customer First Name: "' + str(customer_first_name) + '"')

    app.logger.debug('Customer Last Name: "' + str(customer_last_name) + '"')

    app.logger.debug('Email: "' + str(alias) + '"')

    app.logger.debug('Customer ID: "' + str(customer_id) + '"')

    app.logger.debug('Street Address: "' + str(location_address) + '"')

    app.logger.debug('City: "' + str(location_city) + '"')

    app.logger.debug('State: "' + str(location_state) + '"')

    app.logger.debug('Postal Code: "' + str(location_zip) + '"')

    app.logger.debug('Country Code: "' + str(country_code) + '"')

    network_tags = '"' + company_name.replace(' ', '_') + '", "' + country_code.replace(' ', '_') + '", "' + customer_first_name.replace(' ', '_') + '_' + customer_last_name.replace(' ', '_') + '", "' + alias.replace(' ', '_') + '", "' + ('customer_id_' + str(customer_id)).replace(' ', '_') + '", "' + (location_city).replace(' ', '_') + '", "' + location_state.replace(' ', '_') + '", "Pod_1", "Hub_1"'

    address = location_address + ' ' + location_city + ' ' + location_state + ' ' + str(location_zip)

    payload_tags = "{\"name\":\"" + network_name + "\", \"tags\":[" + network_tags + "], \"address\":\"" + address + "\", \"moveMapMarker\": true}"
    #payload_tags

    headers_tags = {
        'X-Cisco-Meraki-API-Key': "X-Cisco-Meraki-API-Key",
        'Content-Type': "application/json"
        }

    response_tags = requests.request("PUT", url_tags, data=payload_tags, headers=headers_tags)

    while response_tags.status_code == 429:
        attempt = 2
        app.logger.debug(f'Meraki claim WAP Attempt: {attempt}')
        time.sleep(2)
        response_tags = requests.request("PUT", url_tags, data=payload_tags, headers=headers_tags)
        attempt += 1


    return ''










layout = html.Div([
            html.Div([
                html.H2('Assign Asset - Fulfillment Team'),
                html.P('After an order has been approved, this will be used to assign devices to customer locations in Snipe-IT as well as claim the device to the correct Meraki network(if applicable).', style={'fontSize':14})
            ], className='ten columns offset-by-one', style={'margin-top': 10}),
            html.Div([
                html.Div([
                    html.Button('Refresh Orders', id='get_order_button_assign_asset')
                    ], style={'margin-top': 30})], className='ten columns offset-by-one'),
            html.Div(id='table_assign_asset'),
            html.Div([
                html.Div(id='display_selected_row_assign_asset', className='ten columns offset-by-one')
            ]),
            html.Div(id='intermediate-value_assign_asset', style={'display': 'none'})
        ])










@app.callback(output=Output('intermediate-value_assign_asset', 'children'),
    inputs=[Input('get_order_button_assign_asset', "n_clicks")])
def get_order_data(n_clicks):

    app.logger.info('Assign Asset Refreshing Orders...')

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

    filtered_list = df_start.loc[df_start['Status'] == 'Checked']

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

    fulfillment['Ship Address'] = filtered_list['Ship Address']

    fulfillment['Install Address'] = filtered_list['Install Address']

    fulfillment['Ship City'] = filtered_list['Ship City']

    fulfillment['Install City'] = filtered_list['Install City']

    fulfillment['Ship State'] = filtered_list['Ship State']

    fulfillment['Install State'] = filtered_list['Install State']

    fulfillment['Ship Country'] = filtered_list['Ship Country']

    fulfillment['Install Country'] = filtered_list['Install Country']

    fulfillment['Ship Zip'] = filtered_list['Ship Zip']

    fulfillment['Install Zip'] = filtered_list['Install Zip']

    fulfillment['Sale Type'] = filtered_list['Sale Type']

    cleaned_df = fulfillment

    return cleaned_df.to_json()

@app.callback(Output('table_assign_asset', 'children'), [Input('intermediate-value_assign_asset', 'children')])
def orders_table(jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)
        return html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='datatable-interactivity_assign_asset',
                        columns=[
                            {"name": 'Status', "id": 'Status'},
                            {"name": 'Created At', "id": 'Created At'},
                            {"name": 'Internal ID', "id": 'Internal ID'},
                            {"name": 'Invoice #', "id": 'Invoice #'},
                            {"name": 'Processing Bank', "id": 'Processing Bank'},
                            {"name": 'Customer Email', "id": 'Customer Email'},
                            {"name": 'Sales Agent', "id": 'Sales Agent'},
                            {"name": 'First Name', "id": 'First Name'},
                            {"name": 'Last Name', "id": 'Last Name'},
                            {"name": 'Company Name', "id": 'Company Name'},
                            {"name": 'Fulfillment Type', "id": 'Fulfillment Type'},
                            {"name": 'Ship Address', "id": 'Ship Address', "hidden":True},
                            {"name": 'Install Address', "id": 'Install Address', "hidden":True},
                            {"name": 'Ship City', "id": 'Ship City', "hidden":True},
                            {"name": 'Install City', "id": 'Install City', "hidden":True},
                            {"name": 'Ship State', "id": 'Ship State', "hidden":True},
                            {"name": 'Install State', "id": 'Install State', "hidden":True},
                            {"name": 'Ship Country', "id": 'Ship Country', "hidden":True},
                            {"name": 'Install Country', "id": 'Install Country', "hidden":True},
                            {"name": 'Ship Zip', "id": 'Ship Zip', "hidden":True},
                            {"name": 'Install Zip', "id": 'Install Zip', "hidden":True},
                            {"name": 'Sale Type', "id": 'Sale Type', "hidden":True},
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
    output=Output('display_selected_row_assign_asset', "children"),
    inputs=[Input('datatable-interactivity_assign_asset', "selected_rows")],
    state=[State('intermediate-value_assign_asset', 'children'), State('datatable-interactivity_assign_asset', "data")])
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
                                id='display_selected_row_data_table_assign_asset',
                                columns=[
                                    {"name": 'Status', "id": 'Status'},
                                    {"name": 'Created At', "id": 'Created At'},
                                    {"name": 'Internal ID', "id": 'Internal ID'},
                                    {"name": 'Invoice #', "id": 'Invoice #'},
                                    {"name": 'Processing Bank', "id": 'Processing Bank'},
                                    {"name": 'Customer Email', "id": 'Customer Email'},
                                    {"name": 'Sales Agent', "id": 'Sales Agent'},
                                    {"name": 'First Name', "id": 'First Name'},
                                    {"name": 'Last Name', "id": 'Last Name'},
                                    {"name": 'Company Name', "id": 'Company Name'},
                                    {"name": 'Fulfillment Type', "id": 'Fulfillment Type'},
                                    {"name": 'Ship Address', "id": 'Ship Address', "hidden":True},
                                    {"name": 'Install Address', "id": 'Install Address', "hidden":True},
                                    {"name": 'Ship City', "id": 'Ship City', "hidden":True},
                                    {"name": 'Install City', "id": 'Install City', "hidden":True},
                                    {"name": 'Ship State', "id": 'Ship State', "hidden":True},
                                    {"name": 'Install State', "id": 'Install State', "hidden":True},
                                    {"name": 'Ship Country', "id": 'Ship Country', "hidden":True},
                                    {"name": 'Install Country', "id": 'Install Country', "hidden":True},
                                    {"name": 'Ship Zip', "id": 'Ship Zip', "hidden":True},
                                    {"name": 'Install Zip', "id": 'Install Zip', "hidden":True}
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
                                html.Div(dcc.Input(id='input-box-1_assign_asset', type='text', placeholder='Serial #', value='')),
                                html.Div(dcc.Input(id='input-box-2_assign_asset', type='text', placeholder='Tracking #', value='')),
                                html.Button('Submit', id='button_assign_asset'),
                                html.Div(html.H5(id='output-container-button_assign_asset'))
                            ])
                        , className='twelve columns')
                    ])



@app.callback(
    Output('output-container-button_assign_asset', 'children'),
    [Input('button_assign_asset', 'n_clicks')],
    state=[State('input-box-1_assign_asset', 'value'), State('input-box-2_assign_asset', 'value'), State('datatable-interactivity_assign_asset', "selected_rows"), State('intermediate-value_assign_asset', 'children')])
def update_output(n_clicks, serial_num, trk_num, row, jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)

        if n_clicks == None:
            return 'Enter a Serial # and Tracking #, then press submit'
        else:
            if serial_num == '':
                return 'A serial # is needed.'
            else:
                tracking_number = trk_num[-12:]

                selected_row = (fulfillment.iloc[[row[0]]].to_dict("rows"))[0]

                if selected_row.get('Install Address', '') == '':
                    location_address = selected_row['Ship Address']
                else:
                    location_address = selected_row['Install Address']

                if selected_row.get('Install City', '') == '':
                    location_city = selected_row['Ship City']
                else:
                    location_city = selected_row['Install City']

                if selected_row.get('Install State', '') == '':
                    location_state = selected_row['Ship State']
                else:
                    location_state = selected_row['Install State']

                if selected_row.get('Install Country', '') == '':
                    country_code = selected_row['Ship Country']
                else:
                    country_code = selected_row['Install Country']

                if selected_row.get('Install Zip', '') == '':
                    location_zip = selected_row['Ship Zip']
                else:
                    location_zip = selected_row['Install Zip']

                if len(str(location_zip)) == 4:
                    location_zip = '0' + str(location_zip)

                invoice_id = selected_row.get('Invoice #', ' ')

                internal_id = selected_row.get('Internal ID', ' ')

                created_at = selected_row.get('Created At', ' ')

                sales_agent = selected_row.get('Sales Agent', ' ')

                company_name = selected_row.get('Company Name', ' ').replace("'", '')

                customer_first_name = selected_row.get('First Name', ' ')

                customer_last_name = selected_row.get('Last Name', ' ')

                alias = selected_row.get('Customer Email', ' ')

                processing_bank = selected_row.get('Processing Bank', ' ')

                fulfillment_type = selected_row.get('Fulfillment Type', ' ')

                firewalls = ['Firewall', 'MX64', 'MX64W (wireless)', 'MX68', 'MX68 and Wireless Access Point']

                if processing_bank == 'Partner Bank':
                    partner_code = 'Partner Bank 3 Character Code'
                    enable_syslog_tracking = 'True'

                elif processing_bank == 'Partner Bank':
                    partner_code = 'Partner Bank 3 Character Code'
                    enable_syslog_tracking = 'True'

                else:
                    if selected_row.get('Fulfillment Type', '') in firewalls:
                        partner_code = 'MFW'

                    else:
                        partner_code = 'SMB'
                    enable_syslog_tracking = 'False'

                if len(company_name) > 26:
                    too_long_company_name = len(company_name) - 26
                    old_company_name = company_name
                    company_name = (company_name.replace('&', ' ').replace('/', '_')[:-too_long_company_name])
                    app.logger.info('Shortened Location/Network Name from: \'' + old_company_name + '\' to: \'' + company_name + '\'')
                else:
                    pass

                if len(location_city) > 10:
                    too_long_location_city = len(location_city) - 10
                    old_location_city = location_city
                    location_city = (location_city.replace('&', ' ').replace('/', '_')[:-too_long_location_city])
                    app.logger.info('Shortened Location/Network Name from: \'' + old_location_city + '\' to: \'' + location_city + '\'')
                else:
                    pass

                network_tags = company_name.replace(' ', '_') + ' ' + country_code.replace(' ', '_') + ' ' + customer_first_name + '_' + customer_last_name + ' ' + alias.replace(' ', '_') + ' ' + ('customer_id_' + str(internal_id)).replace(' ', '_') + ' ' + location_city.replace(' ', '_') + ' ' + location_state.replace(' ', '_') + ' Pod_1 Hub_1' + ' ' + processing_bank.replace(' ', '_')

                if country_code == 'US':
                    #This sets the variable 'location_name' to be 'company_name - location_city - location_state'
                    location_name = network_name = partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - ' + location_state

                    if len(network_name) > 50:
                        too_long = len(network_name) - 50
                        old_network_name = network_name
                        location_name = network_name = (partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - ' + location_state)
                        app.logger.info('Shortened Location/Network Name from: \'' + old_network_name + '\' to: \'' + network_name + '\'')
                    else:
                        pass

                elif country_code == 'UK':
                    #This sets the variable 'location_name' to be 'company_name - location_city - UK'
                    location_name = network_name = partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - UK'

                    if len(network_name) > 50:
                        too_long = len(network_name) - 50
                        old_network_name = network_name
                        location_name = network_name = (partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - UK')
                        app.logger.info('Shortened Location/Network Name from: \'' + old_network_name + '\' to: \'' + network_name + '\'')
                    else:
                        pass

                else:
                    if location_state == 'Newfoundland':
                        location_state = 'NL'

                    elif location_state == 'Labrador':
                        location_state = 'NL'

                    elif location_state == 'New Brunswick':
                        location_state = 'NB'

                    elif location_state == 'Nova Scotia':
                        location_state = 'NS'

                    elif location_state == 'Prince Edward Island':
                        location_state = 'PE'

                    elif location_state == 'Quebec':
                        location_state = 'QC'

                    elif location_state == 'Nunavut':
                        location_state = 'NU'

                    elif location_state == 'Ontario':
                        location_state = 'ON'

                    elif location_state == 'Manitoba':
                        location_state = 'MB'

                    elif location_state == 'Yukon':
                        location_state = 'YT'

                    elif location_state == 'Alberta':
                        location_state = 'AB'

                    elif location_state == 'Northwest Territories':
                        location_state = 'NT'

                    elif location_state == 'British Columbia':
                        location_state = 'BC'

                    elif location_state == 'Saskatchewan':
                        location_state = 'SK'

                    else:
                        pass

                    #This sets the variable 'location_name' to be 'company_name - location_city - location_state'
                    location_name = network_name = partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - ' + location_state

                    if len(network_name) > 50:
                        too_long = len(network_name) - 50
                        old_network_name = network_name
                        location_name = network_name = (partner_code + ' - ' + company_name.replace('&', ' ').replace('/', '_').replace(',', '') + ' - ' + location_city + ' - ' + location_state)
                        app.logger.info('Shortened Location/Network Name from: \'' + old_network_name + '\' to: \'' + network_name + '\'')
                    else:
                        pass

                app.logger.info('Checking out asset from Snipe-IT...')

                checkout_response = check_out_asset(serial_num, tracking_number, invoice_id, internal_id, location_name)

                if checkout_response == 'error':
                    app.logger.error('There were no locations found using the search term: "' + location_name + '". Please check the Spreadsheet and Snipe-IT for errors and try the search again.')
                    return 'There were no locations found using the search term: "' + location_name + '". Please check the Spreadsheet and Snipe-IT for errors and try the search again.'

                else:
                    try:
                        app.logger.info('Updating asset in Snipe-IT...')

                        update_asset(serial_num, internal_id, invoice_id, tracking_number, processing_bank)

                        if selected_row.get('Sale Type', '') == 'Replacement (support only)':
                            app.logger.info('Replacement Order')

                            app.logger.info('#####PROCESS COMPLETE#####')

                        else:
                            if processing_bank == 'Partner Bank':
                                org_uuid = 'Partner Bank Internal UUID'

                            elif processing_bank == 'Partner Bank':
                                org_uuid = 'Partner Bank Internal UUID'

                            elif processing_bank == 'SecurityMetrics Operations':
                                org_uuid = 'Partner Bank Internal UUID'

                            else:
                                org_uuid = create_new_pulse_org(location_name)

                            if selected_row.get('Fulfillment Type', '') in firewalls:
                                app.logger.info('Assigning device to Meraki Network...')
                                network_id = claim_device_add_tags_meraki_network(serial_num, network_name, company_name, country_code, customer_first_name, customer_last_name, alias, internal_id, location_city, location_state, location_address, location_zip, partner_code)

                                app.logger.info('Setting up Meraki Pulse Internal...')
                                setup_internal_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid, serial_num, 'meraki', network_id, enable_syslog_tracking)

                                app.logger.info('Setting up Meraki Pulse External...')
                                setup_external_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid)

                            elif selected_row.get('Fulfillment Type', '') == 'WAP':
                                app.logger.info('Assigning WAP to Meraki Network...')
                                meraki_claim_tag_wireless_access_point(serial_num, network_name, company_name, country_code, customer_first_name, customer_last_name, alias, internal_id, location_city, location_state, location_address, location_zip, partner_code)

                            elif selected_row.get('Fulfillment Type', '') == '4G Backup ONLY (No other device)':
                                app.logger.info('4G Backup only order...')

                            else:
                                app.logger.info('Finding emvee Collector Identifier...')
                                collector_identifier = find_emvee_collector_identifier(serial_num)

                                app.logger.info('Setting up Collector Pulse Internal...')
                                setup_internal_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid, serial_num, 'emvee', collector_identifier, enable_syslog_tracking)

                                if selected_row.get('Fulfillment Type', '') != 'Vision':
                                    app.logger.info('Setting up Collector Pulse External...')
                                    setup_external_pulse(location_name, location_city, location_state, location_address, location_zip, org_uuid)

                                else:
                                    app.logger.info('Vision Order does not need Pulse External Sensor...')

                        app.logger.info('Updating row on Google Spreadsheet...')

                        update_master_gsheet(created_at, sales_agent, tracking_number, serial_num, fulfillment_type)

                        app.logger.info(('The device with the Serial# "{}" has been checked out to "{}"').format(serial_num, location_name))

                        return ('The device with the Serial# "{}" has been checked out to "{}"').format(serial_num, location_name)

                    except:
                        app.logger.exception('')

                        return ('There was an error with the order')
