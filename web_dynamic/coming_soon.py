#!/usr/bin/python3

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    return render_template('coming_soon.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
