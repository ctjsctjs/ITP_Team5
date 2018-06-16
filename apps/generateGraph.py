from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

from app import app

layout = \
    html.Div([
        # Header
        html.Div([
            html.H1('Generate Graph', className='header-title'),

            # item-button, generate graph
            dcc.Link('Generate Graph', href='/apps/viewGraph', className='button item-element-margin header-button')

        ], className='wrapper-white header-wrapper page-width'),

        # body-wrapper
        html.Div([

            # body-Content
            html.Div([

                # item-wrapper
                html.Div([

                    # item-header
                    html.H2('Graph 1', className='item-element-margin'),

                    # item-row, settings
                    html.Div([
                        dcc.Dropdown(
                            id='app-graph-dropdown',
                            className='item-dropdown item-element-margin',
                            placeholder="Series",
                            options=[
                                {'label': i, 'value': i} for i in [
                                    'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E',
                                    'Parameter F'
                                ]
                            ]),
                        dcc.Dropdown(
                            id='app-graph-dropdown',
                            className='item-dropdown item-element-margin',
                            placeholder="Name",
                            options=[
                                {'label': i, 'value': i} for i in [
                                    'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E',
                                    'Parameter F'
                                ]
                            ]),
                        dcc.Dropdown(
                            id='app-graph-dropdown',
                            className='item-dropdown item-element-margin',
                            placeholder="Mode",
                            options=[
                                {'label': i, 'value': i} for i in [
                                    'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E',
                                    'Parameter F'
                                ]
                            ]),
                    ], className='item-row item-element-margin item-select-height'),

                    # item-row, parameters
                    html.Div([
                        dcc.Dropdown(
                            id='app-graph-dropdown',
                            className='item-dropdown item-element-margin',
                            placeholder="Parameter X",
                            options=[
                                {'label': i, 'value': i} for i in [
                                    'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E',
                                    'Parameter F'
                                ]
                            ]),
                        dcc.Dropdown(
                            id='app-graph-dropdown',
                            className='item-dropdown item-element-margin',
                            placeholder="Parameter Y",
                            options=[
                                {'label': i, 'value': i} for i in [
                                    'Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E',
                                    'Parameter F'
                                ]
                            ])
                    ], className='item-row item-element-margin item-select-height'),

                    # html.Div(id='app-graph-display-value' ),
                ], className='item-wrapper'),

                # item-button, add graph
                dcc.Link('Add Graph', href='#', className='button item-element-margin')

            ], className='content-wrapper page-width')
        ], className='wrapper-grey')
    ])


# @app.callback(
# Output('app-graph-display-value', 'children'),
# [Input('app-graph-dropdown', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)
