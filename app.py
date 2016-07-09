from flask import Flask
from flask import render_template
from flask import abort
from flask import request
from flask import make_response
from datetime import datetime

app = Flask(__name__)

# CURRENT WORKFLOW:
# 1. Add new post to post_list.
# 2. Run munge_posts.py (this rewrites the `post_list.json` datafile used by the d3 timeline).
# 3. Publish!

# Note: Titles are assigned globally but may also be overwritten in the Jinja2 template using a {% posttitle %}
# wrapper.
# Note: The id parameter is used by the Disqus plugin to verify uniqueness.
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
    'new-york-city-tree-density-viz.html'
    ]

post_paths = [post['route'] for post in post_list]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == '':
        return render_template('about.html', most_recent=request.url_root + post_list[len(post_list) - 1]['route'])
    elif path == 'feed':
        rss_xml = render_template('rss.xml')
        response = make_response(rss_xml)
        response.headers['Content-Type'] = 'application/rss+xml'
        return response
    elif path in post_paths:
        index = post_paths.index(path)
        post = post_list[index]
        return render_template('posts/' + post['template'],
                               id=index + 1,
                               date="{0:02d}/{1:02d}/{2}".format(post['date'].month, post['date'].day,
                                                                 post['date'].year),
                               title=post['title'],
                               most_recent=request.url_root + post_list[len(post_list) - 1]['route']
                               )
    elif path in raws_list:
        return render_template('visualizations/' + path)
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
