import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

layout = \
    html.Div([
        html.H1("HELLO"),
        html.Button('Click Here', id='test-big-button'),

        # Template Usage Test
        html.Div(id='test-table-container'),

        # Input Test
        dcc.Input(
            id='test-input',
            className='form-control col-sm-4',
            placeholder='Enter a value...',
            type='text',
            value=''
        ),

        # Dropdown Test
        html.Div([
            dcc.Dropdown(
                id='test-dropdown',
                className='',
                clearable='True',
                options=[
                    {'label': 'Option', 'value': 'option'},
                    {'label': 'Value', 'value': 'value'},
                    {'label': 'DateTime', 'value': 'datetime'}]
            ),
            html.Div(id='test-dropdown-output', className='')
        ], className=''),

        # Hidden Elements
        html.Div(id='test-dump1', style={'display': 'none'}),
        html.Div(id='test-dump2', style={'display': 'none'}),
        html.Div(id='test-dump3', style={'display': 'none'})
    ], className='')

# Input form to obtain text
text_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='text',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='text',
            value=''
        ),
        html.Button('Submit', id='test-submit'),
    ]

# Input form to obtain dropdown option
option_input = \
    html.H1('Option')

# Input form to obtain int/float
value_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='number',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='number',
            value=''
        ),
        html.Button('Submit', id='test-submit')
    ]

# Input form to obtain DataTime
date_input = \
    [
        dcc.Input(
            id='test-input1',
            className='form-control col-sm-4',
            placeholder='Enter Min',
            type='date',
            value=''
        ),
        dcc.Input(
            id='test-input2',
            className='form-control col-sm-4',
            placeholder='Enter Max',
            type='date',
            value=''
        ),
        html.Button('Submit', id='test-submit')
    ]

# Input form to obtain DataTime using Dash Datepicker (NOT WORKING)
# TODO: Decide if worth continuing. Remove if aborted
# datepicker_input = \
#     [
#         dcc.DatePickerRange(
#             id='test-date-picker-range',
#             initial_visible_month=dt.now(),
#             start_date_placeholder_text='Start',
#             end_date_placeholder_text='End'
#         ),
#         html.Button('Submit', id='test-submit-datetime')
#     ]
