# Placeholder method TODO: Remove once deemed unnecessary
def generate_graph2D(dataframe, x_axis, y_axis):
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


def generate_graph2D_actual(dataframe, x_axis, y_axis, dummy):
    return