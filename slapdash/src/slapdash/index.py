import dash_html_components as html
from flask import current_app as server
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from .app import app
from .pages import page_not_found, table_of_contents, snipe_it_in_out, check_asset, assign_asset, ship_asset, update_inventory_manager_sheet, retired_apps, l3_firewall_rules_backup, find_meraki_network_id, l3_firewall_rules_upload, l3_firewall_rules_append_csv, l3_firewall_rules_manual_add
from .components import make_nav, fa
from .utils import get_url


#
# The router
#

# Ordered iterable of routes: tuples of (route, layout), where 'route' is a
# string corresponding to path of the route (will be prefixed with Dash's
# 'routes_pathname_prefix' and 'layout' is a Dash Component.
URLS = (
    ("", table_of_contents.layout),
    ("check_asset", check_asset.layout),
    ("assign_asset", assign_asset.layout),
    ("ship_asset", ship_asset.layout),
    ("find_meraki_network_id", find_meraki_network_id.layout),
    ("l3_firewall_rules_backup", l3_firewall_rules_backup.layout),
    ("l3_firewall_rules_upload", l3_firewall_rules_upload.layout),
    ("l3_firewall_rules_append_csv", l3_firewall_rules_append_csv.layout),
    ("l3_firewall_rules_manual_add", l3_firewall_rules_manual_add.layout),
    ("update_inventory_manager_sheet", update_inventory_manager_sheet.layout),
    ("snipe_it_in_out", snipe_it_in_out.layout),
    ("retired_apps", retired_apps.layout),
)


ROUTES = {get_url(route): layout for route, layout in URLS}


@app.callback(
    Output(server.config["CONTENT_CONTAINER_ID"], "children"),
    [Input("url", "pathname")],
)
def router(pathname):
    """The router"""
    default_layout = page_not_found(pathname)
    return ROUTES.get(pathname, default_layout)


#
# The Navbar
#

# Ordered iterable of navbar items: tuples of `(route, display)`, where `route`
# is a string corresponding to path of the route (will be prefixed with
# URL_BASE_PATHNAME) and 'display' is a valid value for the `children` keyword
# argument for a Dash component (ie a Dash Component or a string).
NAV_ITEMS = (
    ("", html.Div([fa("fas fa-home"), "Home"])),
    ("check_asset", html.Div([fa("fas fa-check-double"), "Check Asset"])),
    ("assign_asset", html.Div([fa("fas fa-shopping-cart"), "Assign Asset"])),
    ("ship_asset", html.Div([fa("fas fa-truck"), "Ship Asset"])),
    ("find_meraki_network_id", html.Div([fa("fas fa-search"), "Find Meraki Network ID"])),
    ("l3_firewall_rules_backup", html.Div([fa("fas fa-download"), "L3 MX Firewall Rules Backup"])),
    ("l3_firewall_rules_upload", html.Div([fa("fas fa-upload"), "L3 MX Firewall Rules Upload"])),
    ("l3_firewall_rules_append_csv", html.Div([fa("fas fa-folder-plus"), "L3 MX Firewall Rules Append CSV"])),
    ("l3_firewall_rules_manual_add", html.Div([fa("fas fa-plus"), "L3 MX Firewall Rules Manual Add"])),
    ("update_inventory_manager_sheet", html.Div([fa("fas fa-wrench"), "Update Inventory Manager Spreadsheet"])),
    ("snipe_it_in_out", html.Div([fa("fas fa-crosshairs"), "Snipe-IT Quick Check In/Out"])),
    ("retired_apps", html.Div([fa("fas fa-undo"), "Retired Apps"])),
)


@app.callback(
    Output(server.config["NAVBAR_CONTAINER_ID"], "children"), [Input("url", "pathname")]
)
def update_nav(pathname):
    """Create the navbar with the current page set to active"""
    if pathname is None:
        # pathname is None on the first load of the app; ignore this
        raise PreventUpdate("Ignoring first url.pathname callback")
    return make_nav(NAV_ITEMS, pathname)
