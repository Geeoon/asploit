import sys
from flask import Flask

app = Flask("Flask Backdoored API")

@app.route("/")
def index():
    return f"""<!doctype html>
<html>
    <head>
        <title>Test Website</title>
    </head>
    <body>
        <h1>Flask Test Site</h1>
        <p>This website is currently infected with the backdoor.</p>
        <p>Running on Python version { '.'.join(map(str, sys.version_info[:3])) }</p>
    </body>
</html>"""

if __name__ == "__main__":
   app.run(debug=True, port=8000)