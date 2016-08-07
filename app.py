from datetime import datetime
from flask import (Flask, render_template, abort, request, make_response)
from static.post_assets.citibike.datastore import DataStore
import json

app = Flask(__name__)

# Initialize the MongoDB connection once.
db = DataStore(uri="mongodb://localhost:27017")


post_list = [
    {
        'title': 'About this website',
        'route': '2015/10/31/this-website.html',
        'date': datetime(2015, 10, 31),
        'template': 'this-website.html',
        'snap': 'this-website.png'
    },
    {
        'title': 'An exercise in probability',
        'route': '2015/11/06/an-exercise-in-probability.html',
        'date': datetime(2015, 11, 6),
        'template': 'an-exercise-in-probability.html',
        'snap': 'an-exercise-in-probability.png'
    },
    {
        'title': 'Measuring Wikipedia Signpost popularity',
        'route': '2016/01/17/signpost-views.html',
        'date': datetime(2016, 1, 17),
        'template': 'signpost-views.html',
        'snap': 'signpost-views.png'
    },
    {
        'title': 'Openness versus quality in the Wikipedia community',
        'route': '2015/12/12/openness-versus-quality.html',
        'date': datetime(2015, 12, 11),
        'template': 'openness-versus-quality.html',
        # 'snap': 'empty.png'
        'snap': 'openness-versus-quality.png'
    },
    {
        'title': 'The decision to launch the Space Shuttle Challenger',
        'route': '2016/02/07/space-shuttle-challenger.html',
        'date': datetime(2016, 2, 7),
        'template': 'space-shuttle-challenger.html',
        'snap': 'space-shuttle-challenger.png'
    },
    {
        'title': 'Is Starbucks really always two blocks away?',
        'route': '2016/02/09/average-chain-distance.html',
        'date': datetime(2016, 2, 9),
        'template': 'average-chain-distance.html',
        'snap': 'average-chain-distance.png'
    },
    {
        'title': 'Exploring the IBM Watson Concept Insights service using watsongraph',
        'route': '2016/02/11/watsongraph-visualization.html',
        'date': datetime(2016, 2, 11),
        'template': 'watsongraph-visualization.html',
        'snap': 'watsongraph-visualization.png'
    },
    {
        'title': 'Analyzing WikiProjects on Wikipedia',
        'route': '2016/02/15/wikiprojects.html',
        'date': datetime(2016, 2, 15),
        'template': 'wikiprojects.html',
        'snap': 'wikiprojects.png'
    },
    {
        'title': 'The executive crisis at the Wikimedia Foundation',
        'route': '2016/02/20/wikimedia-foundation-turnover.html',
        'date': datetime(2016, 2, 20),
        'template': 'wikimedia-foundation-turnover.html',
        'snap': 'wikimedia-foundation-turnover.png'
    },
    {
        'title': 'Addressing traffic fatalities in New York City',
        'route': '2016/03/19/nyc-motor-vehicle-collisions.html',
        'date': datetime(2016, 3, 19),
        'template': 'nyc-motor-vehicle-collisions.html',
        'snap': 'nyc-motor-vehicle-collisions.png'
    },
    {
        'title': 'The worst places to drive in New York City',
        'route': '2016/03/23/worst-places-to-drive.html',
        'date': datetime(2016, 3, 23),
        'template': 'worst-places-to-drive.html',
        'snap': 'worst-places-to-drive.png'
    },
    {
        'title': 'Using the missingno package to visualize missing data',
        'route': '2016/03/28/missingno.html',
        'date': datetime(2016, 3, 28),
        'template': 'missingno.html',
        'snap': 'missingno.png'
    },
    {
        'title': 'Who are the biggest landowners in New York City?',
        'route': '2016/05/27/biggest-landowners-nyc.html',
        'date': datetime(2016, 5, 27),
        'template': 'biggest-landowners-nyc.html',
        'snap': 'landowners.png'
    },
    {
        'title': 'Addressing in New York City',
        'route': '2016/06/01/nyc-addresses.html',
        'date': datetime(2016, 6, 1),
        'template': 'nyc-addresses.html',
        'snap': 'nyc-addresses.png'
    },
    {
        'title': 'Residential property sales in New York City',
        'route': '2016/06/03/residential-property-sales.html',
        'date': datetime(2016, 6, 3),
        'template': 'residential-property-sales.html',
        'snap': 'residential-property-sales.png'
    },
    {
        'title': 'NYC Parks Tree Count Data Jam',
        'route': '2016/06/04/new-york-city-tree-density.html',
        'date': datetime(2016, 6, 4),
        'template': 'new-york-city-tree-density.html',
        'snap': 'new-york-city-real-estate.png'
    },
    {
        'title': 'Null and missing data in Python',
        'route': '2016/06/12/null-and-missing-data-python.html',
        'date': datetime(2016, 6, 12),
        'template': 'null-and-missing-data-python.html',
        'snap': 'null-and-missing-data-python.png'
    },
    {
        'title': 'What are the most popular random seeds?',
        'route': '2016/07/08/randomly-popular.html',
        'date': datetime(2016, 7, 8),
        'template': 'randomly-popular.html',
        'snap': 'randomly-popular.png'
    }
]

raws_list = [
    'challenger-compact-visualization.html',
    'challenger-extended-visualization.html',
    'gregorys-map-visualization.html',
    'dunkin-donuts-map-visualization.html',
    'starbucks-map-visualization.html',
    'manhattan-point-cloud-visualization.html',
    'average-chain-distance-visualization.html',
    'contributions-force-graph-visualization.html',
    'fortune-force-graph-visualization.html',
    'planets-force-graph-visualization.html',
    'biggest-landowners-geo-visualization.html',
    'most-enumerate-landowners-geo-visualization.html',
    'largest-landowners-geo-visualization.html',
    'wealthiest-landowners-geo-visualization.html',
    'longest-streets.html',
    'new-york-city-tree-density-viz.html',
    'life-of-a-citibike.html'
    ]

post_paths = [post['route'] for post in post_list]


@app.route('/')
def main_page():
    return render_template('about.html', most_recent=request.url_root + post_list[len(post_list) - 1]['route'])


@app.route('/feed')
def rss_feed():
    rss_xml = render_template('rss.xml')
    response = make_response(rss_xml)
    response.headers['Content-Type'] = 'application/rss+xml'
    return response


@app.route('/visualizations/<path:path>')
def display_visualization(path):
    return render_template('visualizations/' + path)


@app.route('/citibike-api/<path:path>/id/<int:stationid>')
def citibike_sample(path, stationid):
    if path == 'bike-outbounds':
        collection_name = 'outbound bike trip indices'
    elif path == 'bike-inbounds':
        collection_name = 'inbound bike trip indices'
    elif path == 'outgoing-trips':
        collection_name = 'outgoing trip indicies'
    elif path == 'ingoing-trips':
        collection_name = 'incoming trip indicies'
    else:
        abort(404)
        return
    db = DataStore(uri="mongodb://localhost:27017")
    # Note: str(stationid) not stationid!
    tripset = db.get_station_bikeset(str(stationid), collection_name)
    # Remove None trips---these correspond with trips that have not been populated in the database yet!
    tripset = [trip for trip in tripset if trip is not None]
    # jsonify(tripset) will not work because Flask disallows lists within arrays in top-level JSON, for security
    # reasons. However the security issue in question seems to have been patched out long ago in all major browsers?
    # Further reference: https://github.com/pallets/flask/issues/673;
    # http://flask.pocoo.org/docs/0.11/security/#json-security
    # return jsonify(tripset)
    # json.dumps has no such qualms. It also handles the fact that the output is single-quoted strings, while JSON
    # enforces double-quoted string (so you can't e.g. cast to a straight string using str(tripset)!).
    return json.dumps(tripset)


@app.route('/<path:path>')
def serve(path):
    if path in post_paths:
        index = post_paths.index(path)
        post = post_list[index]
        return render_template('posts/' + post['template'],
                               id=index + 1,
                               date="{0:02d}/{1:02d}/{2}".format(post['date'].month, post['date'].day,
                                                                 post['date'].year),
                               title=post['title'],
                               most_recent=request.url_root + post_list[len(post_list) - 1]['route']
                               )
    else:
        abort(404)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
