import dash_html_components as html


# method to generate table
def generate_table(dataframe):
    table = \
        html.Table([
            # Header
            html.Thead([html.Th(col) for col in dataframe.columns]),
            # Body
            html.Tbody([
                html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                         ]) for i in range(len(dataframe))])
        ], className='filterTable')

    return table
