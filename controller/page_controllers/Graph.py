from dash.dependencies import Input, Output
import pandas as pd

##from model.database import SQL
from view.pages.graph import layout
from view.templates.table import generate_table
from view.templates.graph2D_json import generate_graph2D
from app import app

# Hardcoded Elements TODO: Remove once deemed unnecessary
table_name = 'test-graph-table'


# Obtain data from DataBase
@app.callback(
    Output('graph-table-store', 'children'),
    [Input('graph-dummy', 'children')])
def obtain_data(dummy):
##    sql = SQL()
##    dff = sql.get_table(table_name)

    return 


# Table
@app.callback(
    Output('graph-table-container', 'children'),
    [Input('graph-table-store', 'children')])
def get_table(dff_json):
##    dff = pd.read_json(dff_json)

    return 


# Dropdown options for X-Axis Selection
@app.callback(
    Output('graph-dropdown-x', 'options'),
    [Input('graph-table-store', 'children')])
def create_options_x(dff_json):
##    dff = pd.read_json(dff_json)
    return 


# Dropdown options for Y-Axis Selection
@app.callback(
    Output('graph-dropdown-y', 'options'),
    [Input('graph-table-store', 'children')])
def create_options_y(dff_json):
##    dff = pd.read_json(dff_json)
    return


# Graph
@app.callback(
    Output('graph-graph', 'figure'),
    [Input('graph-table-store', 'children'),
     Input('graph-dropdown-x', 'value'),
     Input('graph-dropdown-y', 'value')])
def get_graph(dff_json, dropdown_x, dropdown_y):
##    dff = pd.read_json(dff_json)
##    return generate_graph2D_actual(dff, dropdown_x, dropdown_y)
    return generateGraphTest()
