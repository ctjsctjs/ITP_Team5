import dash_html_components as html
import dash_core_components as dcc

from config.routes import pathname

navbar = \
    html.Nav([
        html.Div([
            html.Ul([
                html.Li(dcc.Link('Ship Data Analytic System', href=pathname['Home']), className='nav-li'),
                html.Li(dcc.Link('Graphs', href=pathname['Graphs']), className='nav-li'),
                html.Li(dcc.Link('Archive', href=pathname['Archive']), className='nav-li'),
                html.Li(dcc.Link('Database', href=pathname['Database']), className='nav-li'),
                html.Li(dcc.Link('Filter', href=pathname['Filter']), className='nav-li'),
            ], className='nav-ul'),
        ], className='page-width'),
    ], className='nav-wrapper')
