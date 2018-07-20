import dash_html_components as html
import dash_core_components as dcc

from model.database import SQL

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

            html.Div(id='database-upload-dump', style={'display': 'none'}),
            html.Div(id='database-upload-store', style={'display': 'none'}),
            html.Div(id='database-current-table-store', style={'display': 'none'}),

        ], id='database-content-container', className='wrapper-grey'),
        html.Div(id='database-table-container-dump', style={'display': 'none'}),

        html.Div(id='gen-button-dump-store', style={'display': 'none'}),
        html.Div(id='gen-button-dump', style={'display': 'none'})
    ])


def generate_table_container(contents=[]):
    children = [
        html.Div([
            html.H4('Database Tables', className='header-title panel-left table-col-3'),
            html.H4('Status', className='header-title panel-right table-col-3'),
            html.H4('Details', className='header-title panel-left table-col-3'),
            html.H4('Action', className='header-title panel-right table-col-1'),
        ], className='table-heading overflow-auto item-element-margin')
    ]

    status = "In Database"
    for item in contents:
        detail = 'Rows: {}'.format(SQL().get_table_rows(item))
        children.append(
            generate_row(row_name='{}'.format(item), row_id='{}'.format(contents.index(item) + 1), status=status,
                         details=detail,
                         ucode=False))

    return \
        html.Div(
            id='database-tables',
            children=children,
            className='item-wrapper'
        )


def generate_row(row_name, row_id, status, details, ucode=True):
    if ucode:
        row = {
            u'type': u'Div',
            u'namespace': u'dash_html_components',
            u'props': {
                u'className': u'table-row overflow-auto item-element-margin',
                u'children': [
                    {
                        u'type': u'H4',
                        u'namespace': u'dash_html_components',
                        u'props': {
                            u'className': u'header-title table-col-3',
                            u'children': unicode(row_name)
                        }
                    },
                    {
                        u'type': u'H4',
                        u'namespace': u'dash_html_components',
                        u'props': {
                            u'className': u'header-title table-col-3',
                            u'children': unicode(status)
                        }
                    },
                    {
                        u'type': u'H4',
                        u'namespace': u'dash_html_components',
                        u'props': {
                            u'className': u'header-title table-col-3',
                            u'children': unicode(details)
                        }
                    },
                    {
                        u'type': u'Button',
                        u'namespace': u'dash_html_components',
                        u'props': {
                            u'className': u'delete-button item-element-margin margin-right-12',
                            u'children': [
                                {
                                    u'type': u'I',
                                    u'namespace': u'dash_html_components',
                                    u'props': {
                                        u'className': u'fas fa-trash-alt icon',
                                        u'children': None
                                    }
                                },
                                u'Delete'
                            ],
                            u'id': unicode('gen-button-{}'.format(row_id))
                        }
                    }
                ],
                u'id': unicode('gen-row-{}'.format(row_id))
            }
        }

    else:
        row = \
            html.Div([
                html.H4('{}'.format(row_name), className='header-title table-col-3'),
                html.H4('{}'.format(status), className='header-title table-col-3'),
                html.H4('{}'.format(details), className='header-title table-col-3'),
                html.Button([
                    html.I(className="fas fa-trash-alt icon"),
                    'Delete',
                ], className='delete-button item-element-margin margin-right-12',
                    id="gen-button-{}".format(row_id),
                ),
            ], id='gen-row-{}'.format(row_id), className='table-row overflow-auto item-element-margin')

    return row
