import dash_html_components as html
import dash_core_components as dcc

from config.routes import pathname

layout = \
    html.Div([
        # Header
        html.Div([
            html.H1('Archive', className='header-title'),
            dcc.Input(
                placeholder='Search',
                type='text',
                value='',
                className='search-form item-element-margin header-button'
            ),
            html.P('Catalogue of all saved graph settings', className='title-desc'),

        ], className='wrapper-white header-wrapper page-width'),

        # body-wrapper
        html.Div([

            # body-Content
            html.Div([

                # item-wrapper
                html.Div([
                    html.Div([
                        html.H4('Report Name', className='header-title table-col-3'),
                        html.H4('Time', className='header-title table-col-3'),
                        html.H4('Mode', className='header-title table-col-3'),
                        html.H4('Action', className='header-title table-col-1'),
                    ], className='table-heading overflow-auto item-element-margin'),

                    html.Div([
                        html.H4('Relationship of fuel against speed', className='table-col-3'),
                        html.H4('25/08/2018, 15:34:00', className='table-col-3'),
                        html.H4('2D', className='table-col-3'),
                        dcc.Link([
                            html.Button([
                                html.I(className="fas fa-trash-alt icon"),
                                'Delete',
                            ], className='delete-button item-element-margin margin-right-12',
                                id="gen-button-1",
                            ),
                        ], href=pathname['Graphs'], className='header-title table-col-1'),
                    ], className='table-row overflow-auto item-element-margin'),

                    html.Div([
                        html.H4('Relationship of propulsion against speed', className='table-col-3'),
                        html.H4('26/08/2018, 15:54:00', className='table-col-3'),
                        html.H4('3D', className='table-col-3'),
                        dcc.Link([
                            html.Button([
                                html.I(className="fas fa-trash-alt icon"),
                                'Delete',
                            ], className='delete-button item-element-margin margin-right-12',
                                id="gen-button-1",
                            ),
                        ], href=pathname['Graphs'], className='header-title table-col-1'),
                    ], className='table-row overflow-auto item-element-margin'),

                ], className='item-wrapper'),
            ], className='content-wrapper page-width')
        ], className='wrapper-grey')

    ])
