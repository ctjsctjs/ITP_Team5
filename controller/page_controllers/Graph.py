from dash.dependencies import Input, Output
import pandas as pd

from model.database import SQL
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
    sql = SQL()
    dff = sql.get_table(table_name)

    return dff.to_json()


# Table
@app.callback(
    Output('graph-table-container', 'children'),
    [Input('graph-table-store', 'children')])
def get_table(dff_json):
    dff = pd.read_json(dff_json)

    return generate_table(dff)


# Dropdown options for X-Axis Selection
@app.callback(
    Output('graph-dropdown-x', 'options'),
    [Input('graph-table-store', 'children')])
def create_options_x(dff_json):
    dff = pd.read_json(dff_json)
    return [{'label': i, 'value': i} for i in dff.columns]


# Dropdown options for Y-Axis Selection
@app.callback(
    Output('graph-dropdown-y', 'options'),
    [Input('graph-table-store', 'children')])
def create_options_y(dff_json):
    dff = pd.read_json(dff_json)
    return [{'label': i, 'value': i} for i in dff.columns]


# Dropdown options for Y2-Axis Selection
@app.callback(
    Output('graph-dropdown-y2', 'options'),
    [Input('graph-table-store', 'children')])
def create_options_y2(dff_json):
    dff = pd.read_json(dff_json)
    return [{'label': i, 'value': i} for i in dff.columns]

#Graph
@app.callback(
    Output('graph-graph', 'figure'),
    [Input('graph-table-store', 'children'),
     Input('graph-dropdown-x', 'value'),
     Input('graph-dropdown-y', 'value')])
def get_graph(dff_json, dropdown_x, dropdown_y):
    dff = pd.read_json(dff_json)
    return generate_graph2D(dff, dropdown_x, dropdown_y)

#Calculate Differences between 2 y-axis
@app.callback(
    Output('different', 'value'),
    [Input('graph-table-store', 'children'),
     Input('graph-dropdown-y', 'value'),
     Input('graph-dropdown-y2', 'value')])
def calculate_difference(dff_json,dropdown_y,dropdown_y2):
    diff=[]
    dff = pd.read_json(dff_json)
    df1=dff[[dropdown_y,dropdown_y2]]
    for index,row in df1.iterrows():
        diff.append(row[dropdown_y] - row[dropdown_y2])
    return diff
