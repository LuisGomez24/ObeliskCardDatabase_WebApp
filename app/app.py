import base64
import json
import requests
import time
from cachetools import TTLCache
from flask import Flask, render_template, request, redirect, url_for, abort

URL = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
CACHE_SIZE = 2000
CACHE_TTL = 10800

app = Flask(__name__.split('.')[0])
app.secret_key = '87SjpqLnbaUJQ5zcV8ge0w'
cache = TTLCache(maxsize=CACHE_SIZE, ttl=CACHE_TTL)
cache_images = TTLCache(maxsize=CACHE_SIZE*3, ttl=CACHE_TTL)

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
    "Normal" : "",
    "Continuous" : "",
    "Counter" : "",
    "Equip"   : "",
    "Field"   : "", 
    "Quick-Play" : "",
    "Ritual" : ""
}

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
    
    data = json.loads(requests.get(f'{URL}/?fname={card}&num=15&offset=0').text)
    data = set_cache(data)
        
    return render_template('index.html', data=data, card=card)

@app.route('/card/<id>')
def cardview(id):
    card = cache[id]
    #   card['race_image'] = race_images[card['race']]
    if card['frameType'] == 'spell' or card['frameType'] == 'trap':
        card['attribute_image'] = attribute_images[card['frameType'].upper()]
    else:
        card['attribute_image'] = attribute_images[card['attribute']]
    
    return render_template('cardview.html', card=card)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

def set_cache(data):
    for card in data['data']:
        if card['id'] not in cache:
            # If the card is not in the cache, store it
            cache[str(card['id'])] = card
        if card['card_images'][0]['image_url_small'] not in cache_images:
            # If the card image is not in the cache, download and store it in the cache
            card['card_image'] = get_image(card['card_images'][0]['image_url'])
            time.sleep(0.05)
    return data

def get_image(url):
    if url in cache_images:
        # If the image is in the cache, return it directly
        return cache_images[url]
    else:
        # If the image is not in the cache, download it from the API and store it in the cache
        response = requests.get(url)
        image = response.content
        cache_images[url] = base64.b64encode(image).decode('utf-8')
        return cache_images[url]

if __name__ == '__main__':
    app.run()
    