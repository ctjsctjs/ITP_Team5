import dash_html_components as html
import dash_core_components as dcc

layout = \
    html.Div([
        # Header
        html.Div([
            html.H1('Database', className='header-title'),

            # item-button, generate graph
            dcc.Upload(
                id='database-upload-data',
                className='button item-element-margin header-button',
                children=html.Div([
                    html.A('Upload')
                ]),
                # Allow multiple files to be uploaded
                multiple=False
            ),

            html.P('Database Upload and view upload status', className='title-desc'),

            # Hidden upload store
            html.Div(id='database-upload-store')

        ], className='wrapper-white header-wrapper page-width'),

        # body-wrapper
        html.Div([

            # body-Content
            html.Div(
                id='database-table-container',
                className='content-wrapper page-width'),

            # Hidden Table Elements
            html.Div(id='database-table-container-dump', style={'display': 'none'}),
        ], className='wrapper-grey')

    ])


def generate_table_container(contents=[]):
    children = [
        html.Div([
            html.H4('Database Tables', className='header-title panel-left'),
            html.H4('Status', className='header-title panel-right'),
        ], className='table-heading overflow-auto item-element-margin')
    ]

    for item in contents:
        children.append(generate_row(row_name='{}'.format(item), ucode=False))

    return \
        html.Div(
            id='database-tables',
            children=children,
            className='item-wrapper'
        )


def generate_row(row_name, content=None, ucode=True):
    if content is None:
        content = 'Upload Success'

    if ucode:
        row = {
            u'namespace': u'dash_html_components',
            u'type': u'Div',
            u'props': {
                u'className': u'table-row overflow-auto item-element-margin',
                u'children': [
                    {
                        u'namespace': u'dash_html_components',
                        u'type': u'H4',
                        u'props': {
                            u'className': u'header-title panel-left',
                            u'children': unicode(row_name)
                        }
                    },
                    {
                        u'namespace': u'dash_html_components',
                        u'type': u'H4',
                        u'props': {
                            u'className': u'header-title panel-right',
                            u'children': unicode(content)
                        }
                    }
                ]
            }
        }

    else:
        row = \
            html.Div([
                html.H4(row_name, className='header-title panel-left'),
                html.H4(content, className='header-title panel-right'),
            ], className='table-row overflow-auto item-element-margin')

    return row
