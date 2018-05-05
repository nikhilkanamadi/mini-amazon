from flask import render_template
from mini_amazon import app


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', msg='20% cash back on PayPal')
