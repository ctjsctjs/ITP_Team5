import dash
import os

from flask import send_from_directory

app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True

external_css = [
    # 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css'
    'https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css',
    'https://use.fontawesome.com/releases/v5.1.0/css/all.css',
    '/static/css/base.css'
]

external_js = [
    '/static/js/base.js'
]

for css in external_css:
    app.css.append_css({"external_url": css})

for js in external_js:
    app.scripts.append_script({"external_url": js})

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)
