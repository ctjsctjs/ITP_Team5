from dash.dependencies import Input, Output, State
import base64
import io

from view.pages.database import *
from model.database import SQL
from app import app

max_rows = 20


@app.callback(
    Output('gen-button-dump-store', 'children'),
    [Input('gen-button-dump', 'children')])
def load_button_dumps(dump):
    dumps = []
    for n in range(max_rows):
        dumps.append(html.Div(id='gen-button-dump-{}'.format(n + 1), style={'display': 'none'}))

    return dumps


for n in range(max_rows):
    @app.callback(
        Output('gen-button-dump-{}'.format(n + 1), 'children'),
        [Input('gen-button-{}'.format(n + 1), 'n_clicks')],
        [State('gen-row-{}'.format(n + 1), 'children')])
    def delete_button(click, container):
        if click is not None and click != u'None':
            table = container[0]['props']['children']
            SQL().delete_table(table)
        return


# Populate table container with existing tables in database
@app.callback(
    Output('database-table-container', 'children'),
    [Input('database-table-container-dump', 'children')])
def load_table_container(dump):
    return generate_table_container(SQL().get_table_names())


# Obtain user-uploaded file and upload to database
@app.callback(
    Output('database-tables', 'children'),
    [Input('database-upload-data', 'filename')],
    [State('database-tables', 'children'),
     State('database-current-table-store', 'children')])
def upload_excel(table_name, table_container, current_file):
    if table_name is None or table_name == u'None' or unicode(table_name) == current_file:
        pass
    else:
        print(current_file)

        # Format table name
        table_name = __format_filename(table_name)

        # Update table container
        status = "Uploading"
        table_container.append(
            generate_row(
                row_name=table_name,
                row_id='{}'.format(len(table_container)),
                status=status,
                details="Pending"
            )
        )

        print("HELLO")
    return table_container


# Prevents duplicated row upon upload
@app.callback(
    Output('database-current-table-store', 'children'),
    [Input('database-upload-data', 'filename')])
def upload_excel(filename):
    return unicode(filename)


# Obtain user-uploaded file and upload to database
@app.callback(
    Output('database-content-container', 'children'),
    [Input('database-upload-data', 'filename')],
    [State('database-upload-data', 'filename'),
     State('database-upload-data', 'contents'),
     State('database-content-container', 'children')])
def upload_excel(dump, filename, content, container):
    if filename is None or filename == u'None' or content is None or content == u'None':
        pass
    else:
        # Generate Filename
        table_name = __format_filename(filename)

        # Craft Details
        detail = __upload_content(table_name, content)
        detail = __load_details(detail)

        # Craft Status
        status = "Successfully Uploaded"
        status = unicode(status)

        # Update Status and Details
        container[0]['props']['children']['props']['children'].append(generate_row(
            row_name=table_name,
            row_id='{}'.format(len(container[0]['props']['children']['props']['children'])),
            status=status,
            details=detail
        ))

    return container


# Remove extension from filename
def __format_filename(filename):
    return filename.split('.')[0]


# Method to parse uploaded file before use
def __parse_excel(excel_file):
    content_type, content_string = excel_file.split(',')
    decoded = base64.b64decode(content_string)

    return io.BytesIO(decoded)


# Method to create pass/fail details
def __load_details(detail):
    details = "Rows: {} | Truncated: {} | Failed Rows: {}".format(detail['pass'], detail['fail'], detail['failed_rows'])
    return unicode(details)


# Method to upload content to database and return upload result
def __upload_content(table_name, content):
    return SQL().excel_to_sql(table_name=table_name, excel_file=__parse_excel(content))
