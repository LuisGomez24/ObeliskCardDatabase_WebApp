import json
import requests
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_redis import FlaskRedis

app = Flask(__name__.split('.')[0])
redis_client = FlaskRedis(app)
app.secret_key = '87SjpqLnbaUJQ5zcV8ge0w'
URL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

attribute_images = {
    "DARK"   : "https://i.ibb.co/pXMqkkF/Dark.webp"  ,
    "DIVINE" : "https://i.ibb.co/cC3JQ8B/Divine.webp",
    "WIND"   : "https://i.ibb.co/Zfdjhyp/Wind.webp"  ,
    "WATER"  : "https://i.ibb.co/HNL4rDd/Water.webp" ,
    "LIGHT"  : "https://i.ibb.co/L1SFdJ3/Light.webp" ,
    "FIRE"   : "https://i.ibb.co/dsZJgjn/Fire.webp"  ,
    "EARTH"  : "https://i.ibb.co/K24p7X4/Earth.webp" ,
    "SPELL"  : "https://i.ibb.co/XLYk181/Spell.webp" ,
    "TRAP"   : "https://i.ibb.co/fG0j4M3/Trap.webp"
}

race_images = {
    "Normal" : "hola",
    "Continuous" : "",
    "Counter" : "",
    "Equip"   : "",
    "Field"   : "", 
    "Quick-Play" : "",
    "Ritual" : ""
}

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
        try:
            if request.form['card-searched']:
                return redirect(url_for('search', card=request.form['card-searched']), code=302)
        except:
            try:
                if request.form['id']:
                    return redirect(url_for('cardview', id=request.form['id']), code=302)
            except:
                abort(400)
        
        
    data = json.loads(requests.get(f'{URL}/?fname={card}').text)
    return render_template('index.html', data=data, card=card)

@app.route('/card/<id>')
def cardview(id):
    card = json.loads(requests.get(f'{URL}/?id={id}').text)
    #   card['data'][0]['race_image'] = race_images[card['data'][0]['race']]
    if card['data'][0]['frameType'] == 'spell' or card['data'][0]['frameType'] == 'trap':
        card['data'][0]['attribute_image'] = attribute_images[card['data'][0]['frameType'].upper()]
    else:
        card['data'][0]['attribute_image'] = attribute_images[card['data'][0]['attribute']]
    
    print(card['data'][0]['desc'])
    return render_template('cardview.html', card=card['data'][0])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run()