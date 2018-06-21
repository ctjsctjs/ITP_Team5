from dash.dependencies import Input, Output, State, Event
import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

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
                id='app-graph-dropdown-filter',
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
            ], id="filter-field"),

            #items added
            html.Div([], id="filter-list"),

            #item-button, add graph
            html.Button('Add filter', className='button item-element-margin', id="add-filter")
            ], className='item-wrapper', id="item-wrapper"),
        ])
    ], className='content-wrapper page-width')
    ], className='wrapper-grey')
])



#callback for add button
@app.callback(
    Output('filter-list', 'children'),
    [],
    [],
    [Event('add-filter', 'click')]
    )
def display_value():
    newFilter = {"label": "Filter " + str(len(filterList)), "value": str('input')}
    filterList.append(newFilter)
    #print "New Graph settings: " + str(graphSettings) + "\n"

    return html.Div([
        html.H5('Filter List', className='item-element-margin'),
        dcc.Checklist(
        options=filterList,
        values= [i for i in [filterList]],
        labelStyle={'display': 'block'}
    )
], className='item-row item-element-margin item-select-height ', id="item-wrapper-2")
