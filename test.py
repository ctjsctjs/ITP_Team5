import dash
import dash_core_components as dcc
import dash_html_components as html

CWE_borders = {'NL': ['UK', 'NO', 'CWE'],
               'FR': ['ES', 'UK', 'IT_NORTH', 'CH', 'CWE'],
               'DE': ['CH', 'CZ', 'HU', 'SI', 'IT_NORTH', 'DK', 'PL',
                      'SE_4'], }

app = dash.Dash()
app.layout = html.Div([
    html.H1('Model Results'),
    dcc.Tabs(
        tabs=[{'label': i, 'value': i} for i in ['NL', 'FR', 'DE']],
        value='NL',
        id='tabs',
    ),
    html.Div(id='tab-output'),
    html.Div(id='Dynamic Controls'),
    html.Div('OUTPUT'),
    html.Div(id='output-container'),
    html.Div('damnit'),
])


def generate_control_id(value):
    return '{} control'.format(value)


def generate_output_id(value):
    return '{} container'.format(value)


@app.callback(
    dash.dependencies.Output('Dynamic Controls', 'children'),
    [dash.dependencies.Input('tabs', 'value'), ])
def display_controls(c):
    return dcc.Checklist(
        id=generate_control_id(c),
        options=[{'label': i, 'value': i} for i in CWE_borders[c]],
        values=CWE_borders[c])


def generate_output_callback(country):
    def output_callback(borders):
        return '-'.join(borders), country

    return output_callback


app.config.supress_callback_exceptions = True

for country in CWE_borders.keys():
    app.callback(
        dash.dependencies.Output(generate_output_id(country), 'childeren'),
        [dash.dependencies.Input(generate_control_id(country), 'values')])(
        generate_output_callback(country))


@app.callback(
    dash.dependencies.Output('flows', 'children'),
    [dash.dependencies.Input('tabs', 'value'), ])
def update_figure5(country):
    return html.Div(id=generate_output_id(country))


if __name__ == '__main__':
    app.run_server(debug=True)
