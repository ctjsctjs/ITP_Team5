from dash.dependencies import Input, Output, State
import dash_html_components as html
from datetime import datetime as dt

from view.pages.test import layout, value_input, option_input, date_input
from view.templates.table import generate_table
from model.database import SQL
from app import app


# Sample Table Function
def sample_generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# Generate and Populate Table
@app.callback(
    Output('test-table-container', 'children'),
    [Input('test-dump1', 'children')])
def test(dummy):
    test_sql = SQL()
    df = test_sql.get_table("testtable")
    print(df.columns)
    return generate_table(df)

# Input Test
@app.callback(
    Output('test-dump1', 'children'),
    [Input('test-input', 'value')])
def test(input_value):
    print(input_value)


# Dropdown Test
@app.callback(
    Output('test-dropdown-output', 'children'),
    [Input('test-dropdown', 'value')])
def test(value):
    if value == 'option':
        return option_input
    elif value == 'value':
        return value_input
    elif value == 'datetime':
        return date_input


# Read Input Test. Works for int/float and datetime
@app.callback(
    Output('test-dump2', 'children'),
    [Input('test-submit', 'n_clicks')],
    [State('test-input1', 'value'),
     State('test-input2', 'value')])
def test(dump, min_val, max_val):
    print("Min: " + str(min_val))
    print("Max :" + str(max_val))


# Read Date Input Test Using Dash Datepicker (NOT WORKING)
# TODO: Decide if worth continuing. Remove if aborted
# @app.callback(
#     Output('test-dump3', 'children'),
#     [Input('test-submit-datetime', 'n_clicks'),
#      Input('test-date-picker-range', 'start-date'),
#      Input('test-date-picker-range', 'end-date')])
# def test(dump, start, end):
#     print("Start Date: " + str(dt.strptime(start, '%Y-%m-%d')))
#     print("End Date: " + str(dt.strptime(end, '%Y-%m-%d')))

"""
Usable Stuff
"""


# Obtain Vessel Data with dropdown
@app.callback(
    Output('test-dropdown-vessel', 'options'),
    [Input('test-start', 'children')])
def load_dropdown_option_vessel(dump):
    return [{'label': i, 'value': i} for i in SQL().get_vessels()]


# Obtain Vessel Dropdown Input
@app.callback(
    Output('test-dropdown-vessel-store', 'children'),
    [Input('test-dropdown-vessel', 'value')])
def get_result(value):
    print(value)
