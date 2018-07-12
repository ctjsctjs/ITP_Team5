import plotly.graph_objs as go


# Placeholder method TODO: Remove once deemed unnecessary
def generate_graph2D_bar(dataframe, x_axis, y_axis):
    graph2D = {
        'data': [{
            'x': dataframe[x_axis],
            'y': dataframe[y_axis],
            'type': 'bar'
        }],
        'layout': {
            'margin': {
                'l': 20,
                'r': 10,
                'b': 60,
                't': 10
            }
        }
    }

    return graph2D


def generate_graph2D(dataframe, x_axis, y_axis):
    figure = {
        'data': [
            go.Scatter(
                x=dataframe[x_axis],
                y=dataframe[y_axis],
                text='THIS IS A GRAPH',
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name='THIS IS NAME'
            )
        ],
        'layout': go.Layout(
            xaxis={'title': x_axis},
            yaxis={'title': y_axis},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 0},
            hovermode='closest'
        )
    }

    return figure
