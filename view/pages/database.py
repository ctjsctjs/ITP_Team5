import dash_html_components as html
import dash_core_components as dcc

layout = \
    html.Div([
        # Header
        html.Div([
            html.H1('Database', className='header-title'),

            # item-button, generate graph
            dcc.Upload(
                id='upload-data',
                className='button item-element-margin header-button',
                children=html.Div([
                    html.A('Upload')
                ]),
                # Allow multiple files to be uploaded
                multiple=True
            )
        ], className='wrapper-white header-wrapper page-width'),

        # body-wrapper
        html.Div([

            # body-Content
            html.Div([

                # item-wrapper
                html.Div([
                    html.Div([
                        html.H4('Time', className='header-title panel-left'),
                        html.H4('Status', className='header-title panel-right'),
                    ], className='table-heading overflow-auto item-element-margin'),

                    html.Div([
                        html.H4('25/08/2018, 15:34:00', className='header-title panel-left'),
                        html.H4('Upload Success', className='header-title panel-right'),
                    ], className='table-row overflow-auto item-element-margin'),

                    html.Div([
                        html.H4('27/08/2018, 16:35:40', className='header-title panel-left'),
                        html.H4('Upload Success', className='header-title panel-right'),
                    ], className='table-row overflow-auto item-element-margin'),

                ], className='item-wrapper'),
            ], className='content-wrapper page-width')
        ], className='wrapper-grey')

    ])
