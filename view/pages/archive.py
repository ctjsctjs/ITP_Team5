import dash_html_components as html
import dash_core_components as dcc

from config.routes import pathname
#
# layout = \
#     html.Div([
#         # Header
#         html.Div([
#             html.H1('Archive', className='header-title'),
#             dcc.Input(
#                 placeholder='Search',
#                 type='text',
#                 value='',
#                 className='search-form item-element-margin header-button'
#             ),
#             html.P('Catalogue of all saved graph settings', className='title-desc'),
#
#         ], className='wrapper-white header-wrapper page-width'),
#
#         # body-wrapper
#         html.Div([
#
#             # body-Content
#             html.Div([
#
#                 # item-wrapper
#                 html.Div([
#                     html.Div([
#                         html.H4('Report Name', className='header-title table-col-3'),
#                         html.H4('Time', className='header-title table-col-3'),
#                         html.H4('Mode', className='header-title table-col-3'),
#                         html.H4('Action', className='header-title table-col-1'),
#                     ], className='table-heading overflow-auto item-element-margin'),
#
#                     html.Div([
#                         html.H4('Relationship of fuel against speed', className='table-col-3'),
#                         html.H4('25/08/2018, 15:34:00', className='table-col-3'),
#                         html.H4('2D', className='table-col-3'),
#                         dcc.Link([
#                             html.Button([
#                                 html.I(className="fas fa-trash-alt icon"),
#                                 'Delete',
#                             ], className='delete-button item-element-margin margin-right-12',
#                                 id="gen-button-1",
#                             ),
#                         ], href=pathname['Graphs'], className='header-title table-col-1'),
#                     ], className='table-row overflow-auto item-element-margin'),
#
#                     html.Div([
#                         html.H4('Relationship of propulsion against speed', className='table-col-3'),
#                         html.H4('26/08/2018, 15:54:00', className='table-col-3'),
#                         html.H4('3D', className='table-col-3'),
#                         dcc.Link([
#                             html.Button([
#                                 html.I(className="fas fa-trash-alt icon"),
#                                 'Delete',
#                             ], className='delete-button item-element-margin margin-right-12',
#                                 id="gen-button-1",
#                             ),
#                         ], href=pathname['Graphs'], className='header-title table-col-1'),
#                     ], className='table-row overflow-auto item-element-margin'),
#
#                 ], className='item-wrapper'),
#             ], className='content-wrapper page-width')
#         ], className='wrapper-grey')
#
#     ])

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
            html.Div(
                id='read-files-container',
                className='content-wrapper page-width'),

            # Hidden Table Elements
            html.Div(id='read-files-dump', style={'display': 'none'}),
            html.Div(id='test-dump', style={'display': 'none'}),
        ], className='wrapper-grey')
    ])

def generate_files_container(fileList,date,mode):
    return \
    html.Div([
        html.Div([
            html.H4('Report Name', className='header-title table-col-3'),
            html.H4('Time', className='header-title table-col-3'),
            html.H4('Mode', className='header-title table-col-3'),
            html.H4('Action', className='header-title table-col-1'),
        ], className='table-heading overflow-auto item-element-margin'),

        html.Div([
            html.Div([
                html.H4(fileList[n], className='table-col-3'),
                html.H4(date[n], className='table-col-3'),
                html.H4(mode[n], className='table-col-3'),
                html.Button('View', id = 'load-saved-btn-{}'.format(n), className='load-button item-element-margin margin-left-12"'),
                #html.Button('Delete', id='delete-saved-btn-{}'.format(n), className='delete-button item-element-margin "'),
                #store hidden text value to know which file is clicked
                dcc.Input(value=fileList[n], id='hidden-text-{}'.format(n), type='text', style={'display': 'none'}),
                html.Div(id='files-container-{}'.format(n),style={'display':'none'}),
                html.Div(id='global-container',style={'display':'none'}),
            ], className='table-row overflow-auto item-element-margin')
            for n in range(0,len(fileList))
        ], id ='file-list'),
    ])

def generate_empty_container():
    return \
    html.Div([
        html.Div([
            html.H4('Report Name', className='header-title table-col-3'),
            html.H4('Time', className='header-title table-col-3'),
            html.H4('Mode', className='header-title table-col-3'),
            html.H4('Action', className='header-title table-col-1'),
        ], className='table-heading overflow-auto item-element-margin')
    ])
