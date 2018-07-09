from dash.dependencies import Input, Output, State
import base64
import io

from view.pages.database import *
from model.database import SQL
from app import app


sql = SQL()


# Populate table container with existing tables in database
@app.callback(
    Output('database-table-container', 'children'),
    [Input('database-table-container-dump', 'children')])
def load_table_container(dump):
    return generate_table_container(sql.get_table_names())


# Obtain user-uploaded file and upload to database
@app.callback(
    Output('database-tables', 'children'),
    [Input('database-upload-data', 'filename'),
     Input('database-upload-data', 'contents')],
    [State('database-tables', 'children')])
def upload_excel(table_name, excel_file, table_container):
    if table_name is not None:
        # Format table name
        table_name = __format_filename(table_name)

        # Upload to database
        sql.excel_to_sql(table_name=table_name, excel_file=__parse_excel(excel_file))

        # Update table container
        table_container.append(generate_row(row_name=table_name, content='Uploading'))

    return table_container


# # Update table container
# @app.callback(
#     Output('database-tables', 'children'),
#     [Input('database-upload-store', 'children')],
#     [State('database-tables', 'children')])
# def read_container(dump, container):
#     container.append(generate_row())
#     print(container)


# Remove extension from filename
def __format_filename(filename):
    return filename.split('.')[0]


# Method to parse uploaded file before use
def __parse_excel(excel_file):
    content_type, content_string = excel_file.split(',')
    decoded = base64.b64decode(content_string)

    return io.BytesIO(decoded)
