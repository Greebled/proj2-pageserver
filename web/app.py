import os
from flask import Flask, abort, request, render_template, send_from_directory

app = Flask(__name__)

app.url_map.merge_slashes = False
 
PAGES_DIR = os.path.join(app.root_path, "templates")
FORBIDDEN = ("..", "~", "//")
 
 
def raw_request_uri():
    """The URL exactly as the client sent it, before any normalization."""
    env = request.environ
    return env.get("REQUEST_URI") or env.get("RAW_URI") or request.path
 
 
@app.before_request
def check_forbidden():
    uri = raw_request_uri()
    for symbol in FORBIDDEN:
        if symbol in uri:
            abort(403)


@app.route("/")
def hello():
    return "UOCIS docker demo!"

@app.route("/<path:name>")
def serve_page(name):
    path = os.path.join(PAGES_DIR, name)
    if os.path.isfile(path):
        return send_from_directory(PAGES_DIR, name), 200
    abort(404)
 
 
@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403
 
 
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
