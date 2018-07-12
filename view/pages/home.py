import dash_html_components as html
import dash_core_components as dcc
from config.routes import pathname


layout = html.Div([
    html.Div([
        html.Div([
            html.H1('Ship Data Analytic System', className='header-title home-title white'),
            html.P([
            'This system provides tools to facilitate ship analysis, such as Data Visualisation, Data Analytics and more. ',
            'The system aims to provide an effective solution to the ship analysis process, increasing productivity.',
            ],className='title-desc white'),
        ], className='page-width main-padding'),
    ], className='wrapper-img header-wrapper'),

    html.Div([
        html.Div([
            html.Img(src='http://ctjsctjs.com/host/graph-gen.jpg', className='img-1'),
            html.H1('Ship Performance Analysis', className='header-title'),
            html.P([
            'The Ship Performance Analysis provides a Data Visualisation tool that allows the user to generate a meaningful and accurate graph. ',
            'The tool provides full control to the data and filters, allowing the user to control what is shown easily',
            ],className='title-desc'),
            dcc.Link([
                'Start Ship Analysis',
                ], className='button item-element-margin margin-top-24 white-overwrite',
                href=pathname['GenerateGraph']
            )
        ], className='page-width sub-padding'),
    ], className='wrapper-grey header-wrapper'),

    html.Div([
        html.Div([
            html.Img(src='http://ctjsctjs.com/host/graph-gen.jpg', className='img-1'),
            html.H1('Data Analytics', className='header-title'),
            html.P([
            'The Ship Performance Analysis incorporates Data Analytic tools to aid in the accuracy of the graph. ',
            'Different degrees of regression allows the user to determine the best fit line, while Clustering aims to increase the accuracy of the graph.',
            ],className='title-desc'),
            dcc.Link([
                'Start Ship Analysis',
                ], className='button item-element-margin margin-top-24 white-overwrite',
                href=pathname['GenerateGraph']
            )
        ], className='page-width sub-padding'),
    ], className='wrapper-white header-wrapper'),

    html.Div([
        html.Div([
            html.Img(src='http://ctjsctjs.com/host/graph-gen.jpg', className='img-1'),
            html.H1('Data Cleaning', className='header-title'),
            html.P([
            'The system provides a feature for the user to upload an excel file, allowing them to update the database. ',
            'Data cleaning is done to remove any invalid data, providing a dataset that is more meaningful.',
            ],className='title-desc'),
            dcc.Link([
                'Upload a Data file',
                ], className='button item-element-margin margin-top-24 white-overwrite',
                href=pathname['Database']
            )
        ], className='page-width sub-padding'),
    ], className='wrapper-grey header-wrapper'),

    html.Div([
        html.Div([
            html.Img(src='http://ctjsctjs.com/host/graph-gen.jpg', className='img-1'),
            html.H1('Save Settings', className='header-title'),
            html.P([
            'Users are able to save settings and load them through the archives. ',
            'This allows them to easily access commonly used settings easily without having to re-enter the same input.',
            ],className='title-desc'),
            dcc.Link([
                'Visit the archives',
                ], className='button item-element-margin margin-top-12 white-overwrite',
                href=pathname['Archive']
            )
        ], className='page-width sub-padding'),
    ], className='wrapper-white header-wrapper'),

])
