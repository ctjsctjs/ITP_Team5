from dash.dependencies import Input, Output

from controller.page_controllers import Home, GenerateGraph, Archive, Database, Graph, Filter, Test
from view.pages import index
from app import app
from config.routes import *

app.layout = index.layout


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(path):
    if path == pathname['Home']:
        #return Database.layout
        return Home.layout
    elif path == pathname['Graphs']:
        return GenerateGraph.layout
    elif path == pathname['Archive']:
        return Archive.layout
    elif path == pathname['Database']:
        return Database.layout
    elif path == pathname['GenerateGraph']:
        return GenerateGraph.layout
    elif path == pathname['Filter']:
        return Filter.layout
    elif path == pathname['Test']:
        return Test.layout
    else:
        print path
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
