# project_mssapp
This app will be used by the department to help speed up everyday tasks, to  increase efficiency and reduce required work.

## To run:
- cd until you get into the 1st 'slapdash/' folder
- run 'pwd' use displayed path for PATH_TO_SLAPDASH in step 4
- pip install -r requirements.txt
- pip install -e PATH_TO_SLAPDASH
- Change the main path in `main_path.py` to be the path of where the repo has been installed. For example if the repo location is `/path/to/repo/project_mssapp` you will enter `/path/to/repo` into the `main_path.py` file.
- python3 run-flask.py

## Current Features:
- Snipe-IT Quick Check In/Out
  - This app will be used during the Snipe-IT asset data clean up and it will be retired after it is no longer needed. After entering in the "Asset Tag", the "Location Name", and the customer's "Internal ID" the app will go through and check in the device from the user and it will check it out to the location that was specified
- Check Asset - Fulfillment Team
  - After an order has come in, this will be used to check the validity of the order information. If the submitted information is accurate, the necessary records will be created in Snipe-IT and/or Meraki as needed.
- Assign Asset - Fulfillment Team
  - After an order has come in, this will be used to assign devices to customer locations in Snipe-IT, claim the device to the correct Meraki network(if applicable), and creaste the records in Pulse as needed.
- Ship Asset - Fulfillment Team
  - After a device has been taken upstairs to be shipped, this will be used to update the shipdate in Snipe-IT and on the Google Spreadsheet.
- Retired Apps
  - This is where any apps that are no longer needed will go so that they are out of the way but can still be used.

## Planned Features:
- Asset check-in
  - After a device has been returned to us, this app will be used to check-in the device and clear any tags or custom fields that have been added.
  - After a device has been returned, this will be used to mark the asset as deployable stock in Snipe-IT.

What the 'check_asset' page does.
  A. If the information submitted by Sales is correct.
      1. Saves all of the data inputs as variables to use with the different functions.
          A. It determines the partner code to use depending on the bank selected.
              a. If it is a partnered bank then it uses the correct code.
              b. If it is SMB.
                  i. If it is a firewall order it uses 'MFW'
                  ii. If it is not a firewall order it uses 'SMB'
      2. Attempt to create Company record in Snipe-IT
      3. Search Snipe-IT for Company ID
      4. Attempt to create User record in Snipe-IT
      5. Search Snipe-IT for User ID
      6. Attempt to create Location record in Snipe-IT
      7. Search Snipe-IT for Location ID
      8. The app checks if the order is a replacement from support, if it is the check_asset process stops.
      9. If it is not from support it checks if it is a firewall order. If it is, it creates a network in Meraki.
          A. The app sets the "copyFromNetworkId" based on the bank selected by sales.
          B. The app sets the "name" and "productTypes" based on the bank selected.
          C. If the Meraki network is for one of the two special banks then it renames the network from the temp name to the correct name.
      10. The app updates the google spreadsheet saying that the information is Checked with the current date and time as well.

  B. If the information from Sales is incorrect.
      1. The app updates the google spreadsheet saying that there was a sales error and notes the reason for marking it as an error with the date and time.

What the 'assign_asset' page does.
  1. Saves all of the data inputs as variables to use with the different functions.
      A. It determines the partner code to use depending on the bank selected.
          a. If it is a partnered bank then it uses the correct code.
          b. If it is SMB.
              i. If it is a firewall order it uses 'MFW'
              ii. If it is not a firewall order it uses 'SMB'
  2. The app updates the Asset record in Snipe IT with the following.
      A. System internal id
      B. The sales invoice number
      C. The tracking number that is being used with the shipment
      D. The Processing Bank.
  3. The app checks if the order is a replacement from support, if it is the assign_asset process stops.
  4. The app determine the correct Pulse org uuid to use depending on the processing bank submitted.
      A. If it is a partner bank, it uses one of the predefined Pulse org uuids.
      B. If it is not a partner bank, it creates a new organization in the internal SecurityMetrics system for the Company in the order.
  5. The app then makes a check depending on the Fulfillment type.
      A. If the order is a firewall order the app:
          a. claims the device to the correct Meraki network.
          b. updates the tags on that Meraki device.
          c. enables site to site
          d. sets up the CDE vlan with the correct IP address from the list of IP addresses tab of the  google spreadsheet.
          e. creates a location in the correct organization in the internal SecurityMetrics system.
          f. creates an internal sensor.
          g. enables syslog tracking if applicable.
          h. creates an external sensor.
      B. If the order is a WAP order the app:
          a. claims the device to the correct Meraki network.
          b. updates the tags on that Meraki device.
      C. If the order is for a 4G Backup device only the app does not do anything for this step.
      D. The app then does some steps for both vision and collector orders.
          a. finds the emvee for the specific device in the internal SecurityMetrics system.
          b. creates a location in the correct organization in the internal SecurityMetrics system.
          c. creates an internal sensor.
          d. enables syslog tracking if applicable.
          e. if the order is not for a vision device it will create an external sensor.
      E. The app updates the google spreadsheet with the asset serial number and the tracking number and with the current date and time.

What the 'ship_asset' page does.
  1. The app updates the google spreadsheet with the current date and time and the date that the order is shipped out.
