from dash.dependencies import Input, Output, State, Event
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from app import app

filterList = []

layout = html.Div([

#Header
html.Div([
    html.H1('View Graph', className='header-title'),

    #item-button, generate graph
    dcc.Link('Save', href='/apps/viewGraph', className='button item-element-margin header-button'),
    dcc.Link('Export', href='/apps/viewGraph', className='button item-element-margin header-button')

    ], className='wrapper-white header-wrapper page-width'),


    #body-wrapper
    html.Div([

    #body-Content
    html.Div([
        html.Details([
        #item-wrapper
            html.Div([

            #item-header
            html.Div([
                html.H2('Graph name', className='item-element-margin'),
            ], className='item-row item-element-margin item-select-height item-border-bottom'),

            #item-row, settings
            html.Div([
            html.H5('Filters', className='item-element-margin'),
            dcc.Dropdown(
                id='add-filter-input',
                className='item-dropdown item-element-margin',
                placeholder="Filter",
                options=[
                    {'label': i, 'value': i} for i in [
                        'Series', 'Name', 'Date'
                    ]
            ])
            ], className='item-row item-element-margin item-select-height item-border-bottom'),

        #item-row, settings
            html.Div([
                html.H5('Filter', className='item-element-margin')
            ], id="viewGraph-filter-field"),

            #items added
            html.Div([], id="filter-list"),

            #item-button, add graph
            html.Button('Add filter', className='button item-element-margin', id="add-filter-input")
            ], className='item-wrapper', id="item-wrapper"),
        ])
    ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])



#callback for add button
@app.callback(
    Output('filter-list', 'children'),
    [],
    [State('filter-input1', 'value')],
    [Event('add-filter', 'click')]
    )
def display_value(input1, input2):
    newFilter = {"label": "Filter " + str(len(filterList)),"value": str(input1)}
    filterList.append(newFilter)
    print "New Graph settings: " + str(filterList) + "\n"

    return html.Div([
        html.H5('Filter List', className='item-element-margin'),
        dcc.Checklist(
        options=filterList,
        values= [i for i in [filterList]],
        labelStyle={'display': 'block'}
    )
], className='item-row item-element-margin item-select-height ', id="item-wrapper-2")


@app.callback(
    Output('viewGraph-filter-field', 'children'),
    [Input('add-filter-input', 'value')])
def display_value(value):
    if (value=="Series" or value=="Name"):
        return html.Div([
        html.H5('Filters', className='item-element-margin'),
        dcc.Dropdown(
                id='filter-input1',
                className='item-dropdown item-element-margin',
                placeholder="Name",
                options=[
                    {'label': i, 'value': i} for i in [
                        'APL GWANG YANG', 'APL CHONG QING', 'APL LE HAVRE', 'APL QINGDAO'
                    ]
                ])
            ], className='item-row item-element-margin item-select-height item-border-bottom' )
    elif (value=="Date"):
            return html.Div([
            html.H5('Filters', className='item-element-margin'),
            dcc.DatePickerSingle(
                clearable=True,
                with_portal=True,
                date=dt.now()
                ),
            dcc.DatePickerSingle(
                clearable=True,
                with_portal=True,
                date=dt.now()
                )
        ], className='item-row item-element-margin item-select-height item-border-bottom' )
