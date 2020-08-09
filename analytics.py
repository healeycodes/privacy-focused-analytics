import db
import time
import base64
import geoip2.database
from datetime import datetime
from collections import Counter
from flask import Flask, Response, render_template, request, jsonify


app = Flask(__name__)
reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analytics")
def analytics():
    start = int(request.args.get('from', 0))
    end = int(request.args.get('to', 0))
    data = db.load()
    paths = Counter()
    referrers = Counter()
    countries = Counter()
    devices = Counter()
    resolutions = Counter()
    for page_view in data:
        countries[page_view['country']] += 1
        paths[page_view['path']] += 1
        referrers[page_view['referrer']] += 1
        devices[page_view['device']] += 1
        resolutions['{}x{}'.format(
            page_view['width'], page_view['height'])] += 1
    return render_template('analytics.html',
                           start=datetime.fromtimestamp(start).strftime("%c"),
                           end=datetime.fromtimestamp(end).strftime("%c"),
                           paths=paths.most_common(),
                           referrers=referrers.most_common(),
                           countries=countries.most_common(),
                           devices=devices.most_common(),
                           resolutions=resolutions.most_common())


@app.route('/pixel.gif')
def pixel():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    country = ''
    try:
        response = reader.country(ip)
        country = response.country.name
    except geoip2.errors.AddressNotFoundError:
        pass
    device = request.user_agent.browser + ' ' + \
        request.user_agent.version.split('.')[0]

    timestamp = int(time.time())
    path = request.args.get('path', '')
    title = request.args.get('title', '')
    referrer = request.args.get('referrer', '')
    width = int(request.args.get('resolution', '').split(',').pop(0))
    height = int(request.args.get('resolution', '').split(',').pop())

    db.save(timestamp=timestamp,
            path=path,
            title=title,
            referrer=referrer,
            country=country,
            device=device,
            width=width,
            height=height)

    gif = base64.b64decode(  # transparent 1x1 GIF, 43 bytes
        'R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==')
    return Response(gif, mimetype="image/gif")
