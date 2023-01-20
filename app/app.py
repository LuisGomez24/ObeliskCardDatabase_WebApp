import json
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__.split('.')[0])
app.secret_key = '87SjpqLnbaUJQ5zcV8ge0w'
URL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', fname='')
    else:
        return redirect(url_for('search', card=request.form['card-searched']), code=302)

@app.route('/search/<card>', methods=['GET', 'POST'])
def search(card):
    if request.method == 'POST':
        return redirect(url_for('search', card=request.form['card-searched']), code=302)
        
    data = json.loads(requests.get(f'{URL}/?fname={card}').text)
    return render_template('index.html', data=data, card=card)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run()