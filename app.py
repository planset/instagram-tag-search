# coding: utf-8

from flask import Flask
from flask import (
    request, render_template, 
)

from settings import *

from instagram import InstagramAPI 

import re
SMARTPHONE = re.compile(r'(iPhone|iPod|iPad|Android)')

def is_nonmobile(environ):
    if SMARTPHONE.search(environ.get('HTTP_USER_AGENT','')):
        return False
    else:
        return True

app = Flask(__name__)

@app.route('/')
def index():
    if is_nonmobile(request.environ):
        return render_template("index.html")
    else:
        return mindex()

@app.route('/m/')
def mindex():
    return render_template("mindex.html")

@app.route('/tag/<tag>')
def list(tag):
    api = InstagramAPI(client_id=CLIENT_ID)
    items, next = api.tag_recent_media(count=12, tag_name=tag)
    if is_nonmobile(request.environ):
        return render_template("_item.html", items=items)
    else:
        return render_template("_mitem.html", items=items)

@app.route('/m/<tag>')
def mlist(tag):
    app.logger.debug("tag=" + tag)
    api = InstagramAPI(client_id=CLIENT_ID)
    items, next = api.tag_recent_media(count=12, tag_name=tag)
    return render_template("_mitem.html", items=items)

@app.route('/m/item/<id>')
def item(id):
    api = InstagramAPI(client_id=CLIENT_ID)
    item = api.media(media_id=id)
    return render_template("_mimage.html", item=item)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
