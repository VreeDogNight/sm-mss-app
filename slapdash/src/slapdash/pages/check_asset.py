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
import urllib
from main_path import main_path



from ..app import app


app.css.append_css({
    'external_url': 'https://codepen.io/tvreeland-securitymetrics/pen/'
    'drNmGx.css'
})  # noqa: E501



# This sets the creds to come from the 'google_secret.json'
# file that is in the repo with the app
creds = gspread_pandas.conf.get_config(
    conf_dir=f'{main_path}/project_mssapp/',
    file_name='google_secret.json'
)



# This is the API key for the pulseautomation user in Snipe-IT
snipe_it_api_key = 'snipe_it_api_key'

# This is the API key for the pulseautomation user in Meraki
meraki_api_key = 'meraki_api_key'



def updateMasterGsheetYes(created_at, sales_agent, fulfillment_type):
    time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    # This sets the spreadsheet that the code will be working with.
    s_start = Spread(
        'Name of Credentials',
        'Name Of Google Spreadsheet',
        config=creds
    )

    app.logger.debug(s_start)

    app.logger.debug(s_start.sheets)

    # This sets the worksheet in the spreadsheet
    # that the code will be working with.
    data_sheet_start = 'Name of worksheet'

    app.logger.debug(s_start.url)

    # This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)
    #s_start

    # This converts the contents of the worksheet to be a pandas
    # DataFrame so that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    #df_start

    for index, row in df_start.iterrows():
        if row['Created At'] == created_at:
            if row['Sales Agent'] == sales_agent:
                if row['Fulfillment Type'] == fulfillment_type:
                    row_number = str(row.name + 2)

                    if row['Company Name'][-1:] == ' ':
                        if row['Company Name'][:1] == ' ':
                            app.logger.debug('Space at beginning and at the end '
                            'of Company Name. - Created at: ' + row['Created At'])
                            company_name = row['Company Name'][1:-1]
                        else:
                            app.logger.debug('Space just at the end of Company '
                            'Name. - Created at: ' + row['Created At'])
                            company_name = row['Company Name'][:-1]
                    else:
                        if row['Company Name'][:1] == ' ':
                            app.logger.debug('Space just at the beginning of '
                            'Company Name. - Created at: ' + row['Created At'])
                            company_name = row['Company Name'][1:]
                        else:
                            company_name = row['Company Name']


                    if row['Ship City'][-1:] == ' ':
                        if row['Ship City'][:1] == ' ':
                            app.logger.debug('Space at beginning and at the end '
                            'of Ship City. - Created at: ' + row['Created At'])
                            ship_city = row['Ship City'][1:-1]
                        else:
                            app.logger.debug('Space just at the end of Ship '
                            'City. - Created at: ' + row['Created At'])
                            ship_city = row['Ship City'][:-1]
                    else:
                        if row['Ship City'][:1] == ' ':
                            app.logger.debug('Space just at the beginning of Ship '
                            'City. - Created at: ' + row['Created At'])
                            ship_city = row['Ship City'][1:]
                        else:
                            ship_city = row['Ship City']


                    if row['Ship State'][-1:] == ' ':
                        if row['Ship State'][:1] == ' ':
                            app.logger.debug('Space at beginning and at the end of '
                            'Ship State. - Created at: ' + row['Created At'])
                            ship_state = row['Ship State'][1:-1]
                        else:
                            app.logger.debug('Space just at the end of Ship State. '
                            '- Created at: ' + row['Created At'])
                            ship_state = row['Ship State'][:-1]
                    else:
                        if row['Ship State'][:1] == ' ':
                            app.logger.debug('Space just at the beginning of Ship '
                            'State. - Created at: ' + row['Created At'])
                            ship_state = row['Ship State'][1:]
                        else:
                            ship_state = row['Ship State']


                    if row['Install City'][-1:] == ' ':
                        if row['Install City'][:1] == ' ':
                            app.logger.debug('Space at beginning and at the end of '
                            'Install City. - Created at: ' + row['Created At'])
                            install_city = row['Install City'][1:-1]
                        else:
                            app.logger.debug('Space just at the end of Install '
                            'City. - Created at: ' + row['Created At'])
                            install_city = row['Install City'][:-1]
                    else:
                        if row['Install City'][:1] == ' ':
                            app.logger.debug('Space just at the beginning of '
                            'Install City. - Created at: ' + row['Created At'])
                            install_city = row['Install City'][1:]
                        else:
                            install_city = row['Install City']


                    if row['Install State'][-1:] == ' ':
                        if row['Install State'][:1] == ' ':
                            app.logger.debug('Space at beginning and at the end of '
                            'Install State. - Created at: ' + row['Created At'])
                            install_state = row['Install State'][1:-1]
                        else:
                            app.logger.debug('Space just at the end of Install '
                            'State. - Created at: ' + row['Created At'])
                            install_state = row['Install State'][:-1]
                    else:
                        if row['Install State'][:1] == ' ':
                            app.logger.debug('Space just at the beginning of '
                            'Install State. - Created at: ' + row['Created At'])
                            install_state = row['Install State'][1:]
                        else:
                            install_state = row['Install State']


                    new_row_data = [
                        'Checked',
                        row['Created At'].replace("\t", ""),
                        row['Internal ID'].replace("\t", ""),
                        row['Invoice #'].replace("\t", ""),
                        row['Customer Email'].replace("\t", "").replace(" ",""),
                        row['Sales Agent'].replace("\t", ""),
                        row['Processing Bank'].replace("\t", ""),
                        row['First Name'].replace("\t", ""),
                        row['Last Name'].replace("\t", ""),
                        company_name.replace("\t", ""),
                        row['Phone Number'].replace("\t", ""),
                        row['Ship Address'].replace("\t", ""),
                        ship_city.replace("\t", ""),
                        ship_state.replace("\t", ""),
                        row['Ship Zip'].replace("\t", ""),
                        row['Ship Country'].replace("\t", ""),
                        row['Install Address'].replace("\t", ""),
                        install_city.replace("\t", ""),
                        install_state.replace("\t", ""),
                        row['Install Zip'].replace("\t", ""),
                        row['Install Country'].replace("\t", ""),
                        row['Upgrade Response'].replace("\t", ""),
                        row['Fulfillment Type'].replace("\t", ""),
                        row['Firewall Model'].replace("\t", ""),
                        row['Latitude'].replace("\t", ""),
                        row['Longitude'].replace("\t", ""),
                        row['Serial #'].replace("\t", ""),
                        row['Tracking #'].replace("\t", ""),
                        row['Not Checked'].replace("\t", ""),
                        time_stamp.replace("\t", ""),
                        row['Assigned'].replace("\t", ""),
                        row['Shipped'].replace("\t", ""),
                        row['Delivered'].replace("\t", ""),
                        row['Online'].replace("\t", ""),
                        row['Notes'].replace("\t", ""),
                        row['Sale Type'].replace("\t", ""),
                    ]
                    s_start.update_cells(
                        start=(str('A' + row_number)),
                        end=(str('AJ' + row_number)),
                        vals=new_row_data
                    )
        else:
            pass

    return ''



def updateMasterGsheetNo(created_at, sales_agent, reason, fulfillment_type):
    time_stamp = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    # This sets the spreadsheet that the code will be working with.
    s_start = Spread(
        'Name of Credentials',
        'Name Of Google Spreadsheet',
        config=creds
    )

    app.logger.debug(s_start)

    app.logger.debug(s_start.sheets)

    # This sets the worksheet in the spreadsheet
    # that the code will be working with.
    data_sheet_start = 'Name of worksheet'

    app.logger.debug(s_start.url)

    # This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)
    #s_start

    # This converts the contents of the worksheet to be a pandas
    # DataFrame so that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    #df_start

    # #s_start

    for index, row in df_start.iterrows():
        if row['Created At'] == created_at:
            if row['Sales Agent'] == sales_agent:
                if row['Fulfillment Type'] == fulfillment_type:
                    row_number = str(row.name + 2)
                    new_row_data = [
                        'Sales Error',
                        row['Created At'].replace("\t", ""),
                        row['Internal ID'].replace("\t", ""),
                        row['Invoice #'].replace("\t", ""),
                        row['Customer Email'].replace("\t", "").replace(" ",""),
                        row['Sales Agent'].replace("\t", ""),
                        row['Processing Bank'].replace("\t", ""),
                        row['First Name'].replace("\t", ""),
                        row['Last Name'].replace("\t", ""),
                        row['Company Name'].replace("\t", ""),
                        row['Phone Number'].replace("\t", ""),
                        row['Ship Address'].replace("\t", ""),
                        row['Ship City'].replace("\t", ""),
                        row['Ship State'].replace("\t", ""),
                        row['Ship Zip'].replace("\t", ""),
                        row['Ship Country'].replace("\t", ""),
                        row['Install Address'].replace("\t", ""),
                        row['Install City'].replace("\t", ""),
                        row['Install State'].replace("\t", ""),
                        row['Install Zip'].replace("\t", ""),
                        row['Install Country'].replace("\t", ""),
                        row['Upgrade Response'].replace("\t", ""),
                        row['Fulfillment Type'].replace("\t", ""),
                        row['Firewall Model'].replace("\t", ""),
                        row['Latitude'].replace("\t", ""),
                        row['Longitude'].replace("\t", ""),
                        row['Serial #'].replace("\t", ""),
                        row['Tracking #'].replace("\t", ""),
                        row['Not Checked'].replace("\t", ""),
                        time_stamp.replace("\t", ""),
                        row['Assigned'].replace("\t", ""),
                        row['Shipped'].replace("\t", ""),
                        row['Delivered'].replace("\t", ""),
                        row['Online'].replace("\t", ""),
                        reason.replace("\t", ""),
                        row['Sale Type'].replace("\t", ""),
                    ]

                    s_start.update_cells(
                        start=(str('A' + row_number)),
                        end=(str('AJ' + row_number)),
                        vals=new_row_data
                    )
                    app.logger.info(
                        'sales error by: ' + row['Sales Agent'] + ', reason: '
                        + reason
                    )

        else:
            pass

    return ''



def sendToZapier(customer_id, alias, name_first, name_last, company_name,
    phone_number, location_address, location_city, location_state, loc_zip,
    country_code, install_address, install_city, install_state, install_zip,
    install_country_code, fulfillment_type, upgrade_response, bank,
    firewall_model, sale_type):

    url = "https://hooks.zapier.com/hooks/catch/"

    payload = str(
        "{\"customer_id\":\"" + str(customer_id) + "\",\"alias\":\"" + alias
        + "\",\"name_first\":\"" + name_first + "\",\"name_last\":\""
        + name_last + "\",\"company_name\":\"" + company_name
        + "\",\"phone_number\":\"" + str(phone_number)
        + "\",\"location_address\":\"" + location_address
        + "\",\"location_city\":\"" + location_city
        + "\",\"location_state\":\"" + location_state + "\",\"loc_zip\":\""
        + str(loc_zip) + "\",\"country_code\":\"" + country_code
        + "\",\"install_address\":\"" + install_address
        + "\",\"install_city\":\"" + install_city + "\",\"install_state\":\""
        + install_state + "\",\"install_zip\":\"" + str(install_zip)
        + "\",\"install_country_code\":\"" + install_country_code
        + "\",\"fulfillment_type\":\"" + fulfillment_type
        + "\",\"upgrade_response\":\"" + upgrade_response + "\",\"bank\":\""
        + bank + "\",\"firewall_model\":\"" + firewall_model
        + "\",\"sale_type\":\"" + sale_type + "\"}"
    )

    headers = {'Content-Type': 'application/json'}

    response = requests.request("POST", url, data=payload, headers=headers)

    app.logger.debug(response.text)

    return ''



#This defines the function to make a new company in Snipe-IT.
def newCompany(company_name, snipe_it_api_key):
    pay1 = '{"name":"'

    pay2 = '"}'

    pay3 = pay1 + company_name + pay2

    app.logger.debug('Company Name: "' + company_name + '"')

    url = "https://company.snipe-it.io/api/v1/companies"

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipe_it_api_key
    }

    response = requests.post(url, data=pay3, headers=headers)

    app.logger.info(response.text)



#This defines the function to search for companies by name.
def searchCompany(company_name, snipe_it_api_key):

    url = "https://company.snipe-it.io/api/v1/companies"

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipe_it_api_key
    }

    params = (
        ('search', company_name),
    )

    app.logger.debug('Company Name: "' + company_name + '"')

    response = requests.request("GET", url, headers=headers, params=params)

    #This turns response.text into a .json file.
    response_json = json.loads(response.text)

    app.logger.debug(response.text)

    #This grabs the rows section from the response.
    response_list = response_json['rows']

    #This grabs the first item in the rows section.
    response_dict = response_list[0]

    #This grabs the company ID that we need for creating a new user.
    response_int = response_dict['id']

    app.logger.debug('Company ID: "' + str(response_int) + '"')

    return(response_int)



#This defines the function to add a new user in Snipe-IT.
def newUser(name_first, name_last, alias, phone_number, id_company,
    snipe_it_api_key, customer_id):

    url = "https://company.snipe-it.io/api/v1/users"

    pay4 = '{"first_name":"'

    pay5 = '","last_name":"'

    pay6 = '","username":"'

    pay7 = (
        '","password":"multiVariantCharacterPassword","password_confirmation"'
        ':"multiVariantCharacterPassword","phone":"'
    )

    pay8 = '","company_id":'

    pay9 = '}'

    app.logger.debug('First Name: "' + name_first + '"')

    app.logger.debug('Last Name: "' + name_last + '"')

    app.logger.debug('Email: "' + alias + '"')

    app.logger.debug('Phone Number: "' + str(phone_number) + '"')

    app.logger.debug('Company ID: "' + str(id_company) + '"')

    app.logger.debug('Customer ID: "' + str(customer_id) + '"')

    pay10 = (
        pay4 + name_first + pay5 + name_last + pay6 + alias + pay7
        + str(phone_number) + pay8 + str(id_company) + ',"employee_num":"'
        + str(customer_id) + '"' + pay9
    )

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipe_it_api_key
    }

    response = requests.request("POST", url, data=pay10, headers=headers)

    app.logger.info(response.text)



#This defines the function to search for users by username.
def searchUser(user_name, snipe_it_api_key):

    url = "https://company.snipe-it.io/api/v1/users"

    headers = {
        'Content-Type': "application/json",
        'Accept': 'application/json',
        'Authorization': "Bearer " + snipe_it_api_key
    }

    params = (
        ('search', user_name),
    )

    app.logger.debug('Email: "' + user_name + '"')

    response = requests.request("GET", url, headers=headers, params=params)

    app.logger.debug(response.text)

    #This turns response.text into a .json file.
    response_json = json.loads(response.text)

    #This grabs the rows section from the response.
    response_list = response_json['rows']

    #This grabs the first item in the rows section.
    response_dict = response_list[0]

    #This grabs the user ID that we need for creating a new location.
    response_int = response_dict['id']

    app.logger.debug('User ID: "' + str(response_int) + '"')

    return(response_int)



#This defines the function to add a new location in Snipe-IT.
def newLocation(location_name, location_address, location_city,
    location_state, country_code, loc_zip, id_manager, snipe_it_api_key):

    url = "https://company.snipe-it.io/api/v1/locations"

    payload = {
        "name": location_name,
        "address": location_address,
        "city": location_city,
        "state": location_state,
        "country": country_code,
        "zip": loc_zip,
        "manager_id": id_manager
    }

    #This url encodes payload.
    encoded = urllib.parse.urlencode(payload)

    #This changes any + in encoded to %20
    encoded.replace( '+' , "%20")

    headers = {
        'Accept': "application/json",
        'content-type':
        'application/x-www-form-urlencoded',
        'Cache-Control': "no-cache",
        'Authorization': "Bearer " + snipe_it_api_key
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    app.logger.debug('Location Name: "' + location_name + '"')

    app.logger.debug('Location Address: "' + location_address + '"')

    app.logger.debug('Location City: "' + location_city + '"')

    app.logger.debug('Location State: "' + location_state + '"')

    app.logger.debug('Postal Code: "' + loc_zip + '"')

    app.logger.debug('Country Code: "' + country_code + '"')

    app.logger.debug('Manager ID: "' + str(id_manager) + '"')

    app.logger.info(response.text)


    date_time_record_stats = '{0:%Y-%m-%d %H:%M:%S}'.format(
        datetime.datetime.now()
    )

    headers_record_stats = {'Content-type': 'application/json',}

    data_record_stats = (
        '{"date_time":"' + date_time_record_stats + '", "group":"Fulfillment", '
        '"time_saved":"4", "note":"Adding records for Company, User, and '
        'Location in Snipe-IT"}'
    )

    response_record_stats = requests.post(
        'https://hooks.zapier.com/hooks/catch/3803642/vbdkth/',
        headers=headers_record_stats,
        data=data_record_stats
    )


    app.logger.debug('Time saved for fulfillment (in minutes) - 4')




# This defines the function to create a new Meraki Network and to update the
# Master MSS Customer Status Dashboard.
def createMerakiNetwork(network_name, network_timezone, network_tags,
    meraki_api_key, bank):
    url = (
        f"https://api.meraki.com/api/v1/organizations/{organizationId}/"
        "networks"
    )

    if bank == 'Partner Bank':
        network_id = 'PartnerBankCopyFromNetworkId'

    elif bank == 'Partner Bank':
        network_id = 'PartnerBankCopyFromNetworkId'

    elif bank == 'Partner Bank':
        network_id = 'PartnerBankCopyFromNetworkId'

    elif bank == 'Partner Bank':
        network_id = 'PartnerBankCopyFromNetworkId'

    else:
        #This is the network id for the default hardened config.
        network_id = 'N_678917643826109453'

    if bank == 'Partner Bank':
        pay1 = '{"name":"'

        pay2 = '","timeZone": "'

        pay3 = '","tags": "'

        pay4 = '","productTypes": [ "appliance", "wireless" ],"copyFromNetworkId": "'

        pay5 = '"}'

        pay6 = (
            pay1 + "Partner_Bank_Temp_Name" + pay2 + network_timezone + pay3
            + network_tags + pay4 + network_id + pay5
        )

    elif bank == 'Partner Bank':
        pay1 = '{"name":"'

        pay2 = '","timeZone": "'

        pay3 = '","tags": "'

        pay4 = '","productTypes": [ "appliance" ],"copyFromNetworkId": "'

        pay5 = '"}'

        pay6 = (
            pay1 + "Partner_Bank_Temp_Name" + pay2 + network_timezone + pay3
            + network_tags + pay4 + network_id + pay5
        )

    else:
        pay1 = '{"name":"'

        pay2 = '","timeZone": "'

        pay3 = '","tags": "'

        pay4 = '","productTypes": [ "appliance" ],"copyFromNetworkId": "'

        pay5 = '"}'

        pay6 = (
            pay1 + network_name + pay2 + network_timezone + pay3 + network_tags
            + pay4 + network_id + pay5
        )

    app.logger.debug('Network Name: "' + network_name + '"')

    app.logger.debug('Network Time Zone: "' + network_timezone + '"')

    app.logger.debug('Network Tags: "' + network_tags + '"')

    app.logger.debug('Processing Bank: "' + bank + '"')

    headers = {
        'X-Cisco-Meraki-API-Key': meraki_api_key,
        'Content-Type': "application/json"
    }

    response_network = requests.request("POST", url, data=pay6, headers=headers)

    while response_network.status_code == 429:
        attempt = 2
        app.logger.debug(f'Network Create Attempt: "{attempt}"')
        time.sleep(2)
        response_network = requests.request("POST", url, data=pay6, headers=headers)
        attempt += 1

    app.logger.debug(response_network.text)
    data_network = json.loads(response_network.text)

    if data_network.get('errors', '') != '':
        app.logger.info('Creating Meraki Network cancelled')
        app.logger.info(
            'Network creation error: "' + data_network.get('errors', '')[0]
            + '"'
        )

        return (
            'Network creation error: "' + data_network.get('errors', '')[0]
            + '"'
        )
    else:
        app.logger.info('Meraki Network Created')
        app.logger.info(
            'Updating the "Dashboard Grid Fields" worksheet in the Master MSS '
            'Customer Status Dashboard'
        )
        network_id = data_network.get('id', '')

        if bank == 'Partner Bank':
            app.logger.info(
                'Updating network name from Partner_Bank_Temp_Name to '
                + network_name
            )
            url_update_network_name = (
                "https://api.meraki.com/api/v1/networks/" + network_id
            )

            payload_update_network_name = "{\"name\": \"" + network_name + "\"}"

            headers_update_network_name = {
                'Content-Type': "application/json",
                'X-Cisco-Meraki-API-Key': meraki_api_key,
                }

            response_update_network_name = requests.request(
                "PUT", url_update_network_name,
                data=payload_update_network_name,
                headers=headers_update_network_name
            )

            while response_update_network_name.status_code == 429:
                attempt = 2
                app.logger.debug(f'Network Update Attempt: "{attempt}"')
                time.sleep(2)
                response_update_network_name = requests.request(
                    "PUT", url_update_network_name,
                    data=payload_update_network_name,
                    headers=headers_update_network_name
                )
                attempt += 1

            data_update_network_name = json.loads(
                response_update_network_name.text
            )

            if data_update_network_name.get('errors', '') != '':
                app.logger.info('Updating Meraki Network Name Error')
                app.logger.info(
                    'Network rename error: "'
                    + data_update_network_name.get('errors', '')[0] + '"'
                )

                return (
                    'Network rename error: "'
                    + data_update_network_name.get('errors', '')[0] + '"'
                )

            else:
                app.logger.info('Network name Updated')

        elif bank == 'Mooyah':
            app.logger.info(
                'Updating network name from Partner_Bank_Temp_Name to '
                + network_name
            )
            url_update_network_name = (
                "https://api.meraki.com/api/v1/networks/" + network_id
            )

            payload_update_network_name = "{\"name\": \"" + network_name + "\"}"

            headers_update_network_name = {
                'Content-Type': "application/json",
                'X-Cisco-Meraki-API-Key': meraki_api_key,
                }

            response_update_network_name = requests.request(
                "PUT", url_update_network_name,
                data=payload_update_network_name,
                headers=headers_update_network_name
            )

            while response_update_network_name.status_code == 429:
                attempt = 2
                app.logger.debug(f'Network Update Attempt: {attempt}')
                time.sleep(2)
                response_update_network_name = requests.request(
                    "PUT", url_update_network_name,
                    data=payload_update_network_name,
                    headers=headers_update_network_name
                )
                attempt += 1

            data_update_network_name = json.loads(
                response_update_network_name.text
            )

            if data_update_network_name.get('errors', '') != '':
                app.logger.info('Updating Meraki Network Name Error')
                app.logger.info(
                    'Network rename error: "'
                    + data_update_network_name.get('errors', '')[0] + '"'
                )

                return (
                    'Network rename error: "'
                    + data_update_network_name.get('errors', '')[0] + '"'
                )

            else:
                app.logger.info('Network name Updated')

        #This sets the spreadsheet that the code will be working with.
        s = Spread(
            'Name of Credentials',
            'Name Of Google Spreadsheet',
            config=creds
        )

        app.logger.debug(s)

        app.logger.debug(s.sheets)

        data_sheet = 'Name of worksheet'

        app.logger.debug(s.url)

        #This opens the worksheet that was selected.
        s.open_sheet(data_sheet)
        s

        #This converts the contents of the worksheet to be a pandas DataFrame
        #so that the information can be manipulated.
        df = s.sheet_to_df(header_rows=1, index=0).astype(str)
        #print(df)

        #This will go through every row of the DataFrame looking for
        #'Not Assigned' in the column 'Location_Name'
        #When it finds that row, it will replace 'Not Assigned' with the value
        #from the variable network_name
        for index, row in df.iterrows():
            if row['Location Name'] == 'Not Assigned':
                if bank == 'Partner Bank':
                    vpn_nat_ip = row['VPN NAT IP'][:-3] + "/26"
                else:
                    vpn_nat_ip = row['VPN NAT IP']
                new_row_data = [
                    network_name, bank, '', '', '', '', vpn_nat_ip, '', '', '',
                    '', network_id, '', '', ''
                ]
                app.logger.debug('B' + str((int(row['Index']) + 1)))
                #This will change just the data in the first row that says
                #'Not Assigned' in the column 'Location Name'. It will add in
                #the network_name, bank, and network_id the correct columns.
                s.update_cells(
                    start=('B' + str((int(row['Index']) + 1))),
                    end=('P' + str((int(row['Index']) + 1))),
                    vals=new_row_data
                )
                break

        return ''



US_Alaska = ['AK']

US_Arizona = ['AZ']

US_Hawaii = ['HI']

US_Pacific = ['WA','OR','NV','CA']

US_Mountain = ['MT','ID','WY','UT','CO','NM']

US_Central = [
    'MN','ND','SD','WI','NE','IA','IL','KS','MO','KY','OK','AR','TX','LA','TN',
    'MS','AL'
]

US_Eastern = [
    'CT','DE','FL','GA','IN','ME','MD','MA','MI','NH','NJ','NY','NC','OH','PA',
    'RI','SC','VT','VA','WV'
]

CA_Newfoundland = ['Newfoundland','Labrador']

CA_Atlantic = ['New Brunswick','Nova Scotia','Prince Edward Island','Quebec']

CA_Eastern = ['Nunavut','Ontario']

CA_Central = ['Manitoba','Saskatchewan']

CA_Mountain = ['Alberta','Northwest Territories']

CA_Pacific = ['British Columbia','Saskatchewan']










layout = html.Div([
            html.Div([
                html.H2('Check Asset - Fulfillment Team'),
                html.P('After an order has come in, this will be used to check '
                'the accuracy of the information from sales before the '
                'information is sent to the webhooks.', style={'fontSize':14})
            ], className='ten columns offset-by-one', style={'margin-top': 10}),
            html.Div([
                html.Div([
                    html.Button(
                        'Refresh Orders',
                        id='get_order_button_check_asset'
                    )
                    ], style={'margin-top': 30})
                ], className='ten columns offset-by-one'),
            html.Div(id='table_check_asset'),
            html.Div([
                html.Div(
                    id='display_selected_row_check_asset',
                    className='ten columns offset-by-one'
                )
            ]),
            html.Div(
                id='intermediate-value_check_asset',
                style={'display': 'none'}
            )
        ])










@app.callback(output=Output('intermediate-value_check_asset', 'children'),
    inputs=[Input('get_order_button_check_asset', "n_clicks")])
def getOrderData(n_clicks):

    app.logger.info('Check Asset Refreshing Orders...')

    #This sets the spreadsheet that the code will be working with.
    s_start = Spread(
        'Name of Credentials',
        'Name Of Google Spreadsheet',
        config=creds
    )

    app.logger.debug(s_start)

    app.logger.debug(s_start.sheets)

    #This sets the worksheet in the spreadsheet that the code will be working
    #with.
    data_sheet_start = 'Name of worksheet'

    app.logger.debug(s_start.url)

    #This opens the worksheet that was selected.
    s_start.open_sheet(data_sheet_start)
    #s

    #This converts the contents of the worksheet to be a pandas DataFrame so
    #that the information can be manipulated.
    df_start = s_start.sheet_to_df(header_rows=1,index=False).astype(str)

    filtered_list = df_start.loc[df_start['Status'] == 'Not Checked']

    cleaned_df = filtered_list

    return cleaned_df.to_json()



@app.callback(Output('table_check_asset', 'children'), [Input('intermediate-value_check_asset', 'children')])
def orders_table(jsonified_cleaned_data):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)
        return html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='datatable-interactivity_check_asset',
                        columns=[
                            {"name": i, "id": i} for i in fulfillment.columns
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
    output=Output('display_selected_row_check_asset', "children"),
    inputs=[Input('datatable-interactivity_check_asset', "selected_rows")],
    state=[State('intermediate-value_check_asset', 'children'), State('datatable-interactivity_check_asset', "data")])
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
                                id='display_selected_row_data_table_check_asset',
                                columns=[
                                    {"name": i, "id": i} for i in fulfillment.columns
                                ],
                                # data should be a list of dictionaries.
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
                                html.H2('Is this order submission correct?'),
                                html.Div(
                                    dcc.RadioItems(
                                        options=[
                                            {'label': 'Yes', 'value': 'Yes'},
                                            {'label': 'No', 'value': 'No'}
                                        ],
                                        value=[],
                                        labelStyle={
                                            'display': 'inline-block',
                                            'margin': '6px'
                                        },
                                        id='radio_items_check_asset'
                                    )
                                ),
                                html.H2(
                                    'If it is not correct, please enter in why.'
                                ),
                                html.Div(
                                    dcc.Input(
                                        id='input-box-1_check_asset',
                                        type='text',
                                        placeholder='Reason',
                                        value='')
                                ),
                                html.Button('Submit', id='button_check_asset'),
                                html.Div(
                                    html.H5(
                                        id='output-container-button_check_asset'
                                    )
                                )
                            ])
                        , className='twelve columns')
                    ])



@app.callback(
    Output('output-container-button_check_asset', 'children'),
    [Input('button_check_asset', 'n_clicks')],
    state=[State('radio_items_check_asset', 'value'), State('datatable-interactivity_check_asset', "selected_rows"), State('intermediate-value_check_asset', 'children'), State('input-box-1_check_asset', 'value')])
def update_output(n_clicks, yes_or_no, row, jsonified_cleaned_data, reason):
    if jsonified_cleaned_data == None:
        pass
    else:
        fulfillment = pd.read_json(jsonified_cleaned_data)

        if n_clicks == None:
            return 'Select \'Yes\' or \'No\', then press submit.'
        else:
            if yes_or_no == 'Yes':
                selected_row = (fulfillment.iloc[[row[0]]].to_dict("rows"))[0]

                app.logger.info('Loading Variables...')

                try:
                    created_at = selected_row.get(
                        'Created At', ' '
                    ).replace("\t", "").replace("\n", " ")

                    sales_agent = selected_row.get(
                        'Sales Agent', ' '
                    ).replace("\t", "").replace("\n", " ")

                    customer_id = selected_row.get('Internal ID', '')

                    alias = (selected_row.get(
                        'Customer Email', ''
                    )).replace(' ', '').replace("\t", "").replace("\n", " ")

                    name_first = selected_row.get(
                        'First Name', ''
                    ).replace("\t", "").replace("\n", " ")

                    name_last = selected_row.get(
                        'Last Name', ''
                    ).replace("\t", "").replace("\n", " ")

                    customer_full_name = (
                        name_first + '_' + name_last
                    ).replace(" ", "_")

                    phone_number = selected_row.get('Phone Number', '')

                    location_address = selected_row.get(
                        'Ship Address', ''
                    ).replace("\t", "").replace("\n", " ")

                    loc_zip = selected_row.get('Ship Zip', '')

                    country_code = selected_row.get(
                        'Ship Country', ''
                    ).replace("\t", "").replace("\n", " ")

                    install_address = selected_row.get(
                        'Install Address', ''
                    ).replace("\t", "").replace("\n", " ")

                    install_zip = selected_row.get('Install Zip', '')

                    install_country_code = selected_row.get(
                        'Install Country', ''
                    ).replace("\t", "").replace("\n", " ")

                    fulfillment_type = selected_row.get(
                        'Fulfillment Type', ''
                    ).replace("\t", "").replace("\n", " ")

                    upgrade_response = selected_row.get(
                        'Upgrade Response', ''
                    ).replace("\t", "").replace("\n", " ")

                    bank = selected_row.get(
                        'Processing Bank', ''
                    ).replace("\t", "").replace("\n", " ").replace(" ", "_")

                    firewall_model = selected_row.get(
                        'Firewall Model', ''
                    ).replace("\t", "").replace("\n", " ")

                    sale_type = selected_row.get(
                        'Sale Type', ''
                    ).replace("\t", "").replace("\n", " ")


                    if selected_row['Company Name'][-1:] == ' ':
                        if selected_row['Company Name'][:1] == ' ':
                            app.logger.debug(
                            'Space at beginning and at the end of Company '
                            'Name. - Created at: ' + selected_row['Created At']
                            )
                            company_name = selected_row['Company Name'][1:-1].replace("\t", "").replace("\n", " ").replace("'", '')
                        else:
                            app.logger.debug(
                                'Space just at the end of Company Name. - '
                                'Created at: ' + selected_row['Created At']
                            )
                            company_name = selected_row['Company Name'][:-1].replace("\t", "").replace("\n", " ").replace("'", '')
                    else:
                        if selected_row['Company Name'][:1] == ' ':
                            app.logger.debug(
                                'Space just at the beginning of Company Name. '
                                '- Created at: ' + selected_row['Created At']
                            )
                            company_name = selected_row['Company Name'][1:].replace("\t", "").replace("\n", " ").replace("'", '')
                        else:
                            company_name = selected_row['Company Name'].replace("\t", "").replace("\n", " ").replace("'", '')


                    if selected_row['Ship City'][-1:] == ' ':
                        if selected_row['Ship City'][:1] == ' ':
                            app.logger.debug(
                                'Space at beginning and at the end of Ship '
                                'City. - Created at: '
                                + selected_row['Created At']
                            )
                            location_city = selected_row['Ship City'][1:-1].replace("\t", "").replace("\n", " ")
                        else:
                            app.logger.debug(
                                'Space just at the end of Ship City. - Created '
                                'at: ' + selected_row['Created At']
                            )
                            location_city = selected_row['Ship City'][:-1].replace("\t", "").replace("\n", " ")
                    else:
                        if selected_row['Ship City'][:1] == ' ':
                            app.logger.debug(
                                'Space just at the beginning of Ship City. - '
                                'Created at: ' + selected_row['Created At']
                            )
                            location_city = selected_row['Ship City'][1:].replace("\t", "").replace("\n", " ")
                        else:
                            location_city = selected_row['Ship City'].replace("\t", "").replace("\n", " ")


                    if selected_row['Ship State'][-1:] == ' ':
                        if selected_row['Ship State'][:1] == ' ':
                            app.logger.debug(
                                'Space at beginning and at the end of Ship'
                                ' State. - Created at: '
                                + selected_row['Created At']
                            )
                            location_state = selected_row['Ship State'][1:-1].replace("\t", "").replace("\n", " ")
                        else:
                            app.logger.debug(
                                'Space just at the end of Ship State. - Created'
                                ' at: ' + selected_row['Created At']
                            )
                            location_state = selected_row['Ship State'][:-1].replace("\t", "").replace("\n", " ")
                    else:
                        if selected_row['Ship State'][:1] == ' ':
                            app.logger.debug(
                                'Space just at the beginning of Ship State. - '
                                'Created at: ' + selected_row['Created At']
                            )
                            location_state = selected_row['Ship State'][1:].replace("\t", "").replace("\n", " ")
                        else:
                            location_state = selected_row['Ship State'].replace("\t", "").replace("\n", " ")


                    if selected_row['Install City'][-1:] == ' ':
                        if selected_row['Install City'][:1] == ' ':
                            app.logger.debug(
                                'Space at beginning and at the end of Install'
                                ' City. - Created at: '
                                + selected_row['Created At']
                            )
                            install_city = selected_row['Install City'][1:-1].replace("\t", "").replace("\n", " ")
                        else:
                            app.logger.debug(
                                'Space just at the end of Install City. -'
                                ' Created at: ' + selected_row['Created At']
                            )
                            install_city = selected_row['Install City'][:-1].replace("\t", "").replace("\n", " ")
                    else:
                        if selected_row['Install City'][:1] == ' ':
                            app.logger.debug(
                                'Space just at the beginning of Install City. '
                                '- Created at: ' + selected_row['Created At']
                            )
                            install_city = selected_row['Install City'][1:].replace("\t", "").replace("\n", " ")
                        else:
                            install_city = selected_row['Install City'].replace("\t", "").replace("\n", " ")


                    if selected_row['Install State'][-1:] == ' ':
                        if selected_row['Install State'][:1] == ' ':
                            app.logger.debug(
                                'Space at beginning and at the end of Install'
                                ' State. - Created at: '
                                + selected_row['Created At']
                            )
                            install_state = selected_row['Install State'][1:-1].replace("\t", "").replace("\n", " ")
                        else:
                            app.logger.debug(
                                'Space just at the end of Install State. -'
                                ' Created at: ' + selected_row['Created At']
                            )
                            install_state = selected_row['Install State'][:-1].replace("\t", "").replace("\n", " ")
                    else:
                        if selected_row['Install State'][:1] == ' ':
                            app.logger.debug(
                                'Space just at the beginning of Install State.'
                                ' - Created at: ' + selected_row['Created At']
                            )
                            install_state = selected_row['Install State'][1:].replace("\t", "").replace("\n", " ")
                        else:
                            install_state = selected_row['Install State'].replace("\t", "").replace("\n", " ")


                    #This checks the dict key 'Install Address' and if the key
                    #does not exist it enters '' in as the value
                    #If this statement is true it will use the dict key
                    #'Ship Address'
                    if selected_row.get('Install Address', '') == '':

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable
                        #'Ship Address'
                        if selected_row.get('Ship Address', '').replace(
                            '\n', ' '
                        ).replace('"', '')[-1] == ' ':
                            location_address = selected_row.get(
                                'Ship Address', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'Ship Address'
                        else:
                            location_address = selected_row.get(
                                'Ship Address', ''
                            ).replace('\n', ' ').replace('"', '')

                    #If the statement is false it will use the dict key
                    #'Install Address'
                    else:

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable 'Ship
                        #Address'
                        if selected_row.get(
                            'Install Address', ''
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            location_address = selected_row.get(
                                'Install Address', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'Ship Address'
                        else:
                            location_address = selected_row.get(
                                'Install Address', ''
                            ).replace('\n', ' ').replace('"', '')



                    #This checks the dict key 'Install City' and if the key
                    #does not exist it enters '' in as the value
                    #If this statement is true it will use the dict key 'Ship
                    #City'
                    if selected_row.get('Install City', '') == '':

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable 'Ship City'
                        if selected_row.get(
                            'Ship City', ''
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            location_city = selected_row.get(
                                'Ship City', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'Ship City'
                        else:
                            location_city = selected_row.get(
                                'Ship City', ''
                            ).replace('\n', ' ').replace('"', '')

                    #If the statement is false it will use the dict key
                    #'Install City'
                    else:

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable 'Ship City'
                        if selected_row.get(
                            'Install City', ''
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            location_city = selected_row.get(
                                'Install City', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'Ship City'
                        else:
                            location_city = selected_row.get(
                                'Install City', ''
                            ).replace('\n', ' ').replace('"', '')



                    #This checks the dict key 'Install State' and if the key
                    #does not exist it enters '' in as the value
                    #If this statement is true it will use the dict key
                    #'Ship State'
                    if selected_row.get('Install State', '') == '':

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable
                        #'location_state'
                        if selected_row.get(
                            'Ship State', ''
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            location_state = selected_row.get(
                                'Ship State', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'Ship State'
                        else:
                            location_state = selected_row.get(
                                'Ship State', ''
                            ).replace('\n', ' ').replace('"', '')

                    #If the statement is false it will use the dict key
                    #'Install State'
                    else:

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable
                        #'location_state'
                        if selected_row.get(
                            'Install State', ''
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            location_state = selected_row.get(
                                'Install State', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'location_state'
                        else:
                            location_state = selected_row.get(
                                'Install State', ''
                            ).replace('\n', ' ').replace('"', '')



                    #This checks the dict key 'Install Country' and if the
                    #key does not exist it enters '' in as the value
                    #If this statement is true it will use the dict key
                    #'Ship Country'
                    if selected_row.get('Install Country', '') == '':

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable
                        #'country_code'
                        if selected_row.get(
                            'Ship Country', ' '
                        ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            country_code = selected_row.get(
                                'Ship Country', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'country_code'
                        else:
                            country_code = selected_row.get(
                                'Ship Country', ''
                            ).replace('\n', ' ').replace('"', '')

                    #If the statement is false it will use the dict key
                    #'Install Country'
                    else:

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable
                        #'country_code'
                        if selected_row.get('Install Country', '') == '':
                            country_code = selected_row.get(
                                'Install Country', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'country_code'
                        else:
                            country_code = selected_row.get(
                                'Install Country', ''
                            ).replace('\n', ' ').replace('"', '')



                    #This checks the dict key 'Install Zip' and if the key does
                    #not exist it enters '' in as the value
                    #If this statement is true it will use the dict key
                    #'Ship Zip'
                    if selected_row.get('Install Zip', '') == '':

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable 'loc_zip'
                        if str(selected_row.get(
                            'Ship Zip', ''
                        )).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            loc_zip = selected_row.get(
                                'Ship Zip', ''
                            ).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'loc_zip'
                        else:
                            loc_zip = str(selected_row.get(
                                'Ship Zip', ''
                            )).replace('\n', ' ').replace('"', '')

                    #If the statement is false it will use the dict key
                    #'Install Country'
                    else:

                        #This checks to see if the last character in the value
                        #is ' '
                        #If this statement is true, it goes through and removes
                        #the last character at the end of the value then it
                        #checks for and changes any '\n' or '"' that are found
                        #in the value then saves it as the variable 'loc_zip'
                        if str(selected_row.get(
                            'Install Zip', ''
                        )).replace('\n', ' ').replace('"', '')[-1] == ' ':
                            loc_zip = str(selected_row.get(
                                'Install Zip', ''
                            )).replace('\n', ' ').replace('"', '')[:-1]

                        #If the statement is false, it checks for and changes
                        #any '\n' or '"' that are found in the value then saves
                        #it as the variable 'loc_zip'
                        else:
                            loc_zip = str(selected_row.get(
                                'Install Zip', ''
                            )).replace('\n', ' ').replace('"', '')



                    #This checks the dict key 'sale_type' and if the key does
                    #not exist it enters '' in as the value
                    #This checks to see if the last character is ' '
                    #If this statement is true, it goes through and removes the
                    #last character at the end of the value then it checks for
                    #and changes any '\n' or '"' that are found in the value
                    #then saves it as the variable 'alias'
                    if selected_row.get(
                        'Sale Type', ''
                    ).replace('\n', ' ').replace('"', '')[-1] == ' ':
                        sale_type = selected_row.get(
                            'Sale Type', ''
                        ).replace('\n', ' ').replace('"', '')[:-1]

                    #If the statement is false, it checks for and changes any
                    #'\n' or '"' that are found in the value then saves it as
                    #the variable 'alias'
                    else:
                        sale_type = selected_row.get(
                            'Sale Type', ''
                        ).replace('\n', ' ').replace('"', '')



                    if len(loc_zip) == 4:
                        loc_zip = '0' + str(loc_zip)



                    if country_code == 'US':
                        if location_state in US_Alaska:
                            network_timezone = 'US/Alaska'
                        elif location_state in US_Arizona:
                            network_timezone = 'US/Arizona'
                        elif location_state in US_Hawaii:
                            network_timezone = 'US/Hawaii'
                        elif location_state in US_Pacific:
                            network_timezone = 'US/Pacific'
                        elif location_state in US_Mountain:
                            network_timezone = 'US/Mountain'
                        elif location_state in US_Central:
                            network_timezone = 'US/Central'
                        else:
                            network_timezone = 'US/Eastern'

                    elif country_code == 'UK':
                        network_timezone = 'Greenwich'

                    elif country_code == 'CA':
                        if location_state in CA_Newfoundland:
                            network_timezone = 'Canada/Newfoundland'
                        elif location_state in CA_Atlantic:
                            network_timezone = 'Canada/Atlantic'
                        elif location_state in CA_Eastern:
                            network_timezone = 'Canada/Eastern'
                        elif location_state in CA_Central:
                            network_timezone = 'Canada/Central'
                        elif location_state in CA_Mountain:
                            network_timezone = 'Canada/Mountain'
                        else:
                            network_timezone = 'Canada/Pacific'

                    else:
                        network_timezone = 'Europe/Lisbon'

                    if bank == 'Partner Bank':
                        partner_code = 'Partner Bank 3 Character Code'

                    elif bank == 'Partner Bank':
                        partner_code = 'Partner Bank 3 Character Code'

                    else:
                        firewalls = [
                            'Firewall', 'MX64', 'MX64W (wireless)', 'MX68',
                            'MX68 and Wireless Access Point'
                        ]
                        if selected_row.get('Fulfillment Type', '') in firewalls:
                            partner_code = 'MFW'

                        else:
                            partner_code = 'SMB'

                    network_tags = (
                        company_name.replace(' ', '_') + ' '
                        + country_code.replace(' ', '_') + ' '
                        + customer_full_name.replace(' ', '_') + ' '
                        + alias.replace(' ', '_') + ' '
                        + ('customer_id_' + str(customer_id)).replace(' ', '_')
                        + ' ' + location_city.replace(' ', '_') + ' '
                        + location_state.replace(' ', '_') + ' '
                        + firewall_model.replace(' ', '_')
                        + ' Pod_1 Hub_1' + ' ' + bank.replace(' ', '_')
                    ).replace(',','')

                    if len(company_name) > 26:
                        too_long_company_name = len(company_name) - 26
                        old_company_name = company_name
                        company_name = (company_name.replace('&', ' ').replace('/', '_')[:-too_long_company_name])
                        app.logger.info(
                            'Shortened Location/Network Name from: \''
                            + old_company_name + '\' to: \'' + company_name
                            + '\''
                        )
                    else:
                        pass

                    if len(location_city) > 10:
                        too_long_location_city = len(location_city) - 10
                        old_location_city = location_city
                        location_city = (location_city.replace('&', ' ').replace('/', '_')[:-too_long_location_city])
                        app.logger.info(
                            'Shortened City Name from: \'' + old_location_city
                            + '\' to: \'' + location_city + '\''
                        )
                    else:
                        pass

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

                except:
                    app.logger.exception('')
                    return ('There was an error loading the variables.')



                # try:
                #     sendToZapier(
                #         customer_id, alias, name_first, name_last,
                #         company_name, phone_number, location_address,
                #         location_city, location_state, loc_zip, country_code,
                #         install_address, install_city, install_state,
                #         install_zip, install_country_code, fulfillment_type,
                #         upgrade_response, bank, firewall_model, sale_type
                #     )
                # except:
                #     app.logger.exception('')

                app.logger.debug('Customer ID: "' + str(customer_id) + '"')

                app.logger.debug('Email: "' + alias + '"')

                app.logger.debug('First Name: "' + name_first + '"')

                app.logger.debug('Last Name: "' + name_last + '"')

                app.logger.debug('Company Name: "' + company_name + '"')

                app.logger.debug(
                    'Customer Location/Network Name: "' + location_name + '"'
                )

                app.logger.debug('Phone Number: "' + str(phone_number) + '"')

                app.logger.debug('Ship Address: "' + location_address + '"')

                app.logger.debug('Ship City: "' + location_city + '"')

                app.logger.debug('Ship State: "' + location_state + '"')

                app.logger.debug('Ship Zip: "' + str(loc_zip) + '"')

                app.logger.debug('Ship Country Code: "' + country_code + '"')

                app.logger.debug('Install Address: "' + install_address + '"')

                app.logger.debug('Install City: "' + install_city + '"')

                app.logger.debug('Install State: "' + install_state + '"')

                app.logger.debug('Install Zip: "' + str(install_zip) + '"')

                app.logger.debug(
                    'Install Country: "' + install_country_code + '"'
                )

                app.logger.debug('Fulfillment Type: "' + fulfillment_type + '"')

                app.logger.debug('Upgrade Response: "' + upgrade_response + '"')

                app.logger.debug('Processing Bank: "' + bank + '"')

                app.logger.debug('Firewall Model: "' + firewall_model + '"')

                app.logger.debug('Sale Type: "' + sale_type + '"')

                app.logger.info('Variables Loaded')

                app.logger.info('Creating Company...')

                try:
                    #This runs the function 'newCompany()' with the variable
                    #'company_name'
                    newCompany(company_name, snipe_it_api_key)
                except:
                    app.logger.exception('')
                    return ('There was an error creating a new company in '
                    'Snipe-IT')

                app.logger.info('Company Created.')

                app.logger.info('Searching for company ID...')

                try:
                    #This runs the function 'searchCompany()' with the
                    #variable 'company_name' and saves the returned value to be
                    #the variable 'id_company' to be used later.
                    id_company = searchCompany(company_name, snipe_it_api_key)
                except:
                    app.logger.exception('')
                    return ('There was an error searching for the company in '
                    'Snipe-IT')

                app.logger.info('Company ID Found')

                app.logger.info('Creating New User...')

                try:
                    #This runs the function 'newUser()' with the variables
                    #'name_first', 'name_last', 'alias', 'phone_number',
                    #'id_company', 'snipe_it_api_key', and 'customer_id'.
                    newUser(
                        name_first, name_last, alias, phone_number, id_company,
                        snipe_it_api_key, customer_id
                    )
                except:
                    app.logger.exception('')
                    return ('There was an error creating a new user in '
                    'Snipe-IT')

                app.logger.info('New User created')

                app.logger.info('Searching for user ID...')

                try:
                    #This runs the function 'searchUser()' with the variables
                    #'alias' and 'snipe_it_api_key' and saves the returned
                    #value to be the variable 'id_manager' to be used later.
                    id_manager = searchUser(alias, snipe_it_api_key)
                except:
                    app.logger.exception('')
                    return ('There was an error searching for the user in '
                    'Snipe-IT')

                app.logger.info('User ID found')

                app.logger.info('Creating New Location...')

                try:
                    #This runs the function 'newLocation()' with the variables
                    #'location_name', 'location_address', 'location_city',
                    #'location_state', 'country_code', 'loc_zip', 'id_manager',
                    #and 'snipe_it_api_key'.
                    newLocation(
                        location_name, location_address, location_city,
                        location_state, country_code, loc_zip, id_manager,
                        snipe_it_api_key
                    )
                except:
                    app.logger.exception('')
                    return ('There was an error with creating the location in '
                    'Snipe-IT.')

                app.logger.info('Location created')

                firewalls = [
                    'Firewall', 'MX64', 'MX64W (wireless)', 'MX68',
                    'MX68 and Wireless Access Point'
                ]

                if sale_type == 'Replacement (support only)':
                    app.logger.info('Replacement Order')

                else:
                    if fulfillment_type in firewalls:

                        try:
                            #This runs the function 'createMerakiNetwork()'
                            #with the variables 'network_name',
                            #'network_timezone', 'network_tags', and
                            #'meraki_api_key'.
                            network_create_status = createMerakiNetwork(
                                network_name, network_timezone, network_tags,
                                meraki_api_key, bank
                            )

                            if network_create_status != '':
                                return ('There was an error with creating the '
                                'Meraki Network.')
                        except:
                            app.logger.exception('')
                            return ('There was an error with creating the '
                            'Meraki Network.')

                    else:
                        app.logger.info('Not a Firewall Order')

                app.logger.info(
                    'Updating Master Gsheet row correct', selected_row
                )

                try:
                    updateMasterGsheetYes(created_at, sales_agent, fulfillment_type)
                except:
                    app.logger.exception('')
                    return ('There was an error updating the Master Google '
                    'Sheet')


                return ('This order was marked as correct. Please refresh the '
                'orders.')

            elif yes_or_no == 'No':
                if reason == '':
                    return ('Please enter a reason for why this order '
                    'submission is incorrect.')

                else:
                    app.logger.info('Updating Master Gsheet row incorrect...')

                    selected_row = (
                        fulfillment.iloc[[row[0]]].to_dict("rows")
                    )[0]

                    created_at = selected_row.get(
                        'Created At', ' '
                    ).replace("\t", "").replace("\n", " ")

                    sales_agent = selected_row.get(
                        'Sales Agent', ' '
                    ).replace("\t", "").replace("\n", " ")

                    fulfillment_type = selected_row.get(
                        'Fulfillment Type', ' '
                    ).replace("\t", "").replace("\n", " ")

                    try:
                        updateMasterGsheetNo(created_at, sales_agent, reason, fulfillment_type)
                    except:
                        app.logger.exception('')

                    return ('This order was marked as incorrect and the reason '
                    'was logged. Please refresh the orders.')
            else:
                return 'Select \'Yes\' or \'No\', then press submit.'
