
from dash.dependencies import Input, Output, State

from view.pages.archive import layout
from app import app
from view.pages.archive import generate_empty_container, generate_files_container

import os
import json

# PATH of your Proj TODO CHANGE PATH TO YOUR PROJ PATH
# path = 'C:/Users/YC/Documents/GitHub/ITP_Team5(UI)/'
filesLength = 10
@app.callback(
    Output('read-files-container', 'children'),
    [Input('read-files-dump', 'value')])
def display_value(value):
    # read only .txt files in archive folder store as global
    arr_txt = [x for x in os.listdir('archive') if x.endswith(".txt")]
    if arr_txt != []:
        savedName = []
        savedMode = []
        savedDate = []
        # for files in archive directory, read and obtain mode, date and graph name to display
        for item in arr_txt:
            file = open('archive/' + item, 'r')
            dictionaryFile = json.loads(file.read())[0]
            savedMode.append(dictionaryFile.get('param')[0])
            savedDate.append(dictionaryFile.get('dateTime'))
            if dictionaryFile.get('graphName') == "":
                savedName.append('(Empty File Name)')
            else:
                savedName.append(dictionaryFile.get('graphName'))
        return generate_files_container(savedName, savedDate, savedMode)
    else:
        return generate_empty_container()


def button_callback(noOfFiles):
    @app.callback(
        Output('files-container-{}'.format(noOfFiles), 'children'),
        [Input('load-saved-btn-{}'.format(noOfFiles), 'n_clicks'),
         Input('hidden-text-{}'.format(noOfFiles), 'value')])
    def clicked_filename(loadBtn, filename):
        if loadBtn > 0:
            print ("Hi")
            print filename
            return filename


for k in range(0, filesLength):
    button_callback(k)

filename_inputs = []
for n in range(0, filesLength):
    filename_inputs.append(Input('files-container-{}'.format(n), 'value'))

@app.callback(
    Output('global-container','children'),
    filename_inputs)
def return_filename(*filename_inputs):
    print ("bye")
    print (filename_inputs)
    return filename_inputs
