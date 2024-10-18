from flask import Flask, jsonify, render_template, url_for
import os

app = Flask(__name__)

m7 = None

def App(modulo7, port=3333):
    global m7
    m7 = modulo7

    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    app.run(port=port, debug=True)

def compile_javascript():
    path = os.path.join(os.path.dirname(__file__), "static", "scripts")

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    all_js_files = []
    for file in files:
        file_name = "scripts/" + file
        all_js_files.append(url_for('static', filename = file_name))

    return(all_js_files)

def compile_css():
    path = os.path.join(os.path.dirname(__file__), "static", "styles")

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    all_css_files = []
    for file in files:
        file_name = "styles/" + file
        all_css_files.append(url_for('static', filename = file_name))

    return(all_css_files)

@app.route('/')
def index():
    js_files = compile_javascript()
    css_files = compile_css()
    return render_template('index.html', js_files=js_files, css_files=css_files)

@app.route('/api/graph')
def get_graph():
    data = m7.get_graph()
    return jsonify(data)

@app.route('/api/connections')
def get_connections():
    data = m7.get_connections()
    return jsonify(data)

@app.route('/api/path/<p_id>')
def get_path(p_id):
    data = m7.get_path(p_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)