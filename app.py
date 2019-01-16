from datetime import datetime
from flask import (Flask, render_template, abort, request, make_response, Response, send_from_directory, redirect, url_for)
from static.post_assets.citibike.citibike_trips import DataStore
import json
import os

app = Flask(__name__)
basepath = os.path.abspath(".")

# Initialize the MongoDB connection (for CitiBike).
# db = DataStore(uri="mongodb://localhost:27017")  # Desktop.
db = DataStore(json.load(open(basepath + "/static/post_assets/citibike/mlab_instance_api_key.json"))['uri'])  # mLab

post_list = [
    {
        'title': 'An exercise in probability',
        'route': '2015/11/06/an-exercise-in-probability.html',
        'template': 'an-exercise-in-probability.html',
        'snap': 'an-exercise-in-probability.png',
        'type': 'technical'
    },
    {
        'title': 'Measuring Wikipedia Signpost popularity',
        'route': '2016/01/17/signpost-views.html',
        'template': 'signpost-views.html',
        'snap': 'signpost-views.png',
        'type': 'exploration'
    },
    {
        'title': 'The decision to launch the Space Shuttle Challenger',
        'route': '2016/02/07/space-shuttle-challenger.html',
        'template': 'space-shuttle-challenger.html',
        'snap': 'space-shuttle-challenger.png',
        'type': 'exploration'
    },
    {
        'title': 'Is Starbucks really always two blocks away?',
        'route': '2016/02/09/average-chain-distance.html',
        'template': 'average-chain-distance.html',
        'snap': 'average-chain-distance.png',
        'type': 'exploration'
    },
    {
        'title': 'Exploring the IBM Watson Concept Insights service using watsongraph',
        'route': '2016/02/11/watsongraph-visualization.html',
        'template': 'watsongraph-visualization.html',
        'snap': 'watsongraph-visualization.png',
        'type': 'exploration'
    },
    {
        'title': 'Analyzing WikiProjects on Wikipedia',
        'route': '2016/02/15/wikiprojects.html',
        'template': 'wikiprojects.html',
        'snap': 'wikiprojects.png',
        'type': 'exploration'
    },
    {
        'title': 'The executive crisis at the Wikimedia Foundation',
        'route': '2016/02/20/wikimedia-foundation-turnover.html',
        'template': 'wikimedia-foundation-turnover.html',
        'snap': 'wikimedia-foundation-turnover.png',
        'type': 'exploration'
    },
    {
        'title': 'Addressing traffic fatalities in New York City',
        'route': '2016/03/19/nyc-motor-vehicle-collisions.html',
        'template': 'nyc-motor-vehicle-collisions.html',
        'snap': 'nyc-motor-vehicle-collisions.png',
        'type': 'exploration'
    },
    {
        'title': 'The worst places to drive in New York City',
        'route': '2016/03/23/worst-places-to-drive.html',
        'template': 'worst-places-to-drive.html',
        'snap': 'worst-places-to-drive.png',
        'type': 'exploration'
    },
    {
        'title': 'Using the missingno package to visualize missing data',
        'route': '2016/03/28/missingno.html',
        'template': 'missingno.html',
        'snap': 'missingno.png',
        'type': 'technical'
    },
    {
        'title': 'Who are the biggest landowners in New York City?',
        'route': '2016/05/27/biggest-landowners-nyc.html',
        'template': 'biggest-landowners-nyc.html',
        'snap': 'landowners.png',
        'type': 'exploration'
    },
    {
        'title': 'Addressing in New York City',
        'route': '2016/06/01/nyc-addresses.html',
        'template': 'nyc-addresses.html',
        'snap': 'nyc-addresses.png',
        'type': 'exploration'
    },
    {
        'title': 'Residential property sales in New York City',
        'route': '2016/06/03/residential-property-sales.html',
        'template': 'residential-property-sales.html',
        'snap': 'residential-property-sales.png',
        'type': 'exploration'
    },
    {
        'title': 'Counting New York City street trees',
        'route': '2016/06/04/new-york-city-tree-density.html',
        'template': 'new-york-city-tree-density.html',
        'snap': 'new-york-city-real-estate.png',
        'type': 'exploration'
    },
    {
        'title': 'Null and missing data in Python',
        'route': '2016/06/12/null-and-missing-data-python.html',
        'template': 'null-and-missing-data-python.html',
        'snap': 'null-and-missing-data-python.png',
        'type': 'advocacy'
    },
    {
        'title': 'What are the most popular random seeds?',
        'route': '2016/07/08/randomly-popular.html',
        'template': 'randomly-popular.html',
        'snap': 'randomly-popular.png',
        'type': 'technical'
    },
    {
        'title': 'The anatomy of an open data portal',
        'route': '2016/08/11/nyc-open-data-portal.html',
        'template': 'nyc-open-data-portal.html',
        'snap': 'nycopendata.png',
        'type': 'exploration'
    },
    {
        'title': 'The making of Life of Citi Bike',
        'route': '2016/08/27/day-in-the-life-of-citibike.html',
        'template': 'day-in-the-life-of-citibike.html',
        'snap': 'life-of-citibike-alt.png',
        'type': 'technical'
    },
    {
        'title': 'Bringing D3.JS to Jupyter Notebook with Py-D3',
        'route': '2016/09/12/py-d3.html',
        'template': 'py-d3.html',
        'snap': 'py-d3.png',
        'type': 'technical'
    },
    {
        'title': 'Mapping Citi Bike routes',
        'route': '2016/09/14/citibike-map.html',
        'template': 'citibike-map.html',
        'snap': 'citibike-map.png',
        'type': 'exploration'
    },
    {
        'title': 'Saving progress in pandas',
        'route': '2016/10/29/saving-progress-pandas.html',
        'template': 'saving-progress-pandas.html',
        'snap': 'saving-progress-pandas.png',
        'type': 'technical'
    },
    {
        'title': 'In context: phase 2 of the Second Avenue Subway',
        'route': '2017/01/12/second-avenue-subway.html',
        'template': 'second-avenue-subway.html',
        'snap': 'second-avenue-subway.png',
        'type': 'exploration'
    },
    {
        'title': 'Geospatial visualization made easy with geoplot',
        'route': '2017/02/07/geoplot.html',
        'template': 'geoplot.html',
        'snap': 'geoplot.png',
        'type': 'technical'
    },
    {
        'title': 'Two million calls to 311',
        'route': '2017/02/13/311.html',
        'template': '311.html',
        'snap': '311.png',
        'type': 'exploration'
    },
    {
        'title': 'Parsing subway rides with gtfs-tripify',
        'route': '2018/01/29/gtfs-tripify.html',
        'template': 'gtfs-tripify.html',
        'snap': 'gtfs-tripify.png',
        'type': 'technical'
    },
    {
        'title': 'Kaggle kernels are Turing complete',
        'route': '2018/02/25/kaggle-kernels-are-turing-complete.html',
        'template': 'kaggle-kernels-are-turing-complete.html',
        'snap': 'kaggle-kernels-are-turing-complete.png',
        'type': 'technical'
    },
    {
        'title': 'Designing data visualization APIs',
        'route': '2018/05/30/dataviz-apis.html',
        'template': 'dataviz-apis.html',
        'snap': 'dataviz-apis.png',
        'type': 'technical'
    },
    {
        'title': 'Tennis\'s wooden spoons',
        'route': '2018/06/10/tennis-wooden-spoons.html',
        'template': '/tennis-wooden-spoons.html',
        'snap': 'tennis-wooden-spoons.png',
        'type': 'exploration'
    },
    {
        'title': 'What next for open data?',
        'route': '2018/06/17/what-next-for-open-data.html',
        'template': '/what-next-for-open-data.html',
        'snap': 'what-next-for-open-data.png',
        'type': 'advocacy'
    },
    {
        'title': 'My approach to solving coding challenges',
        'route': '2018/08/14/solving-algorithms.html',
        'template': '/solving-algorithms.html',
        'snap': 'code-writer-snap.png',
        'type': 'technical'
    },
    {
        'title': 'Finding a model for collaboration in govtech that works',
        'route': '2018/08/19/finding-a-model-for-collaboration.html',
        'template': '/finding-a-model-for-collaboration.html',
        'snap': 'code-writer-snap.png',
        'type': 'advocacy'
    },
    {
        'title': 'Building an MTA historical train arrival application',
        'route': '2018/08/29/subway-explorer.html',
        'template': 'subway-explorer.html',
        'snap': 'code-writer-snap.png',
        'type': 'technical'
    },
    {
        'title': 'The three kinds of data scientists',
        'route': '2018/10/18/roles-in-data-science.html',
        'template': 'roles-in-data-science.html',
        'snap': 'code-writer-snap.png',
        'type': 'advocacy'
    },
    {
        'title': 'One year of taking notes with Jupyter on the cloud',
        'route': '2019/01/01/taking-notes-on-the-cloud.html',
        'template': 'taking-notes-on-the-cloud.html',
        'snap': 'code-writer-snap.png',
        'type': 'advocacy'
    },
    {
        'title': 'Mapping Ford Go Bike trips in the Bay Area',
        'route': '2019/01/15/ford-go-bike-maps.html',
        'template': 'ford-go-bike-maps.html',
        'snap': 'code-writer-snap.png',
        'type': 'exploration'
    }
]

post_paths = [post['route'] for post in post_list]
technical_posts = [post for post in post_list if post['type'] == 'technical']
exploratory_posts = [post for post in post_list if post['type'] == 'exploration']
advocacy_posts = [post for post in post_list if post['type'] == 'advocacy']

project_list = [
    {
        'title': 'missingno',
        'description': 'A missing data visualization library',
        'snap': 'missingno.png',
        'links': [
            {'title': 'Using missingno to visualize missing data',
             'href': './2016/03/28/missingno.html',
             'type': 'post'},
            {'title': 'JOSS paper',
             'href': 'http://joss.theoj.org/papers/52b4115d6c03864b884fbf3334851322',
             'type': 'paper'},
            {'title': 'Try it',
             'href': 'https://github.com/ResidentMario/missingno',
             'type': 'repo'}
        ]
    },
    {
        'title': 'life of citi bike',
        'description': 'Exploring a day in the life of Citi Bike',
        'snap': 'life-of-citibike-alt.png',
        'links': [
            {'title': 'The making of Life of Citi Bike',
             'href': './2016/08/27/day-in-the-life-of-citibike.html',
             'type': 'post'
             },
            {'title': 'Try it',
             'href': 'http://www.residentmar.io/visualizations/life-of-citibike.html',
             'type': 'webapp'}
        ]
    },
    {
        'title': 'py_d3',
        'description': 'Port of the D3.JS visualization grammar to Jupyter',
        'snap': 'py-d3.png',
        'links': [
            {'title': 'Bringing D3.JS to Jupyter Notebook with Py-D3',
             'href': './2016/09/12/py-d3.html',
             'type': 'post'},
            {'title': 'Try it',
             'href': 'https://github.com/ResidentMario/py_d3',
             'type': 'repo'}
        ]
    },
    {
        'title': 'checkpoints',
        'description': 'A progress-saving pandas monkey-patch',
        'snap': 'saving-progress-pandas.png',
        'links': [
            {'title': 'Saving progress in pandas',
             'href': './2016/10/29/saving-progress-pandas.html',
             'type': 'post'},
            {'title': 'Try it',
             'href': 'https://github.com/ResidentMario/checkpoints',
             'type': 'repo'}
        ]
    },
    {
        'title': 'geoplot',
        'description': 'A geospatial data visualization library',
        'snap': 'geoplot.png',
        'links': [
            {'title': 'Geospatial visualization made easy with geoplot',
             'href': './2017/02/07/geoplot.html',
             'type': 'post'},
            {'title': 'Documentation',
             'href': 'https://residentmario.github.io/geoplot/index.html',
             'type': 'docs'},
            {'title': 'Try it',
             'href': 'https://github.com/ResidentMario/geoplot',
             'type': 'repo'}
        ]
    },
    {
        'title': 'subway explorer',
        'description': 'What real-time arrival data says about your commute',
        'snap': 'subway-explorer.png',
        'links': [
            {'title': 'Building an MTA historical train arrival application',
             'href': './2018/05/16/subway-explorer.html',
             'type': 'post'},
            {'title': 'Parsing subway rides with gtfs-tripify',
             'href': './2018/01/29/gtfs-tripify.html',
             'type': 'post'},
            {'title': 'Repo',
             'href': 'https://github.com/ResidentMario/subway-explorer-webapp',
             'type': 'repo'}
        ]
    },
    {
        'title': 'kaggle learn',
        'description': 'Two tracks in an online data science learning platform',
        'snap': 'kaggle-learn.png',
        'links': [
            {'title': 'Overview',
             'href': 'https://www.kaggle.com/learn',
             'type': 'link'},
            {'title': 'Try the pandas track',
             'href': 'https://www.kaggle.com/learn/pandas'},
            {'title': 'Try the data visualization track',
             'href': 'https://www.kaggle.com/learn/data-visualisation',
             'type': 'link'}
        ]
    },
    {
        'title': 'the machine learning repository',
        'description': 'Organized notes on machine learning',
        'snap': 'the-machine-learning-repository.png',
        'links': [
            {'title': 'Try it',
             'href': 'https://residentmario.github.io/machine-learning-notes/index.html',
             'type': 'webapp'}
        ]
    }
]


advocacy_list = [
    {
        'title': 'Who runs the world? Data',
        'route': 'https://www.amny.com/opinion/columnists/mark-chiusano/who-run-the-world-data-says-aleksey-bilogur-1.11863032'
    },
    {
        'title': 'NYC City Council testimony on open data',
        'route': 'https://www.youtube.com/watch?v=U7T2Hwj3vjc'
    },
    {
        'title': 'Implementing good design',
        'route': 'https://github.com/ResidentMario/implementing-good-design'
    },
    {
        'title': 'Becoming a civic technologist out of college',
        'route': 'https://blog.codingitforward.com/becoming-a-civic-technologist-out-of-college-4bcb37f9777c',
    },
    {
        'title': 'Learning by doing with data viz blogging',
        'route': 'https://github.com/ResidentMario/data-visualization-blogging'
    },
    {
        'title': 'Kaggle site documentation',
        'route': 'https://www.kaggle.com/docs'
    },
    {
        'title': 'Profiling top Kagglers: Bestfitting, currently #1 in the world',
        'route': 'http://blog.kaggle.com/2018/05/07/profiling-top-kagglers-bestfitting-currently-1-in-the-world/'
    }
]


@app.route('/')
def main_page():
    return render_template('home.html',
                           technical_posts=technical_posts,
                           exploratory_posts=exploratory_posts,
                           advocacy_posts=advocacy_posts,
                           project_list=project_list)


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/blog.html')
def blog():
    f = request.args.get('filter')
    current_filters = [f] if f else ['technical', 'exploration', 'advocacy']
    print(current_filters)

    return render_template(
        'blog.html',
        post_list=json.dumps(post_list[::-1]),
        current_filters=current_filters
    )


@app.route('/projects.html')
def projects():
    return render_template('projects.html',
                           project_list=project_list,
                           advocacy_list=advocacy_list)


@app.route('/latest.html')
def latest_post():
    return redirect(request.url_root + post_list[len(post_list) - 1]['route'], code=302)


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
        collection_name = 'outgoing trip indices'
    elif path == 'incoming-trips':
        collection_name = 'incoming trip indices'
    else:
        abort(404)
        return
    tripset = db.get_station_bikeset(stationid, collection_name)
    # Remove None trips---these correspond with trips that have not been populated in the database yet!
    tripset = [trip for trip in tripset if trip is not None]
    return Response(json.dumps(tripset), mimetype='application/json')


@app.route('/geoplot/<path:path>')
def serve_geoplot_documentation(path):
    return redirect("https://residentmario.github.io/geoplot/index.html")


@app.route('/<path:path>')
def serve(path):
    if path in post_paths:
        index = post_paths.index(path)
        post = post_list[index]
        date_str = post['route'][:10]
        year, month, day = date_str[:4], date_str[5:7], date_str[8:10]
        return render_template('posts/' + post['template'],
                               id=index + 1,
                               date="{0}/{1}/{2}".format(month, day, year),
                               title=post['title']
                              )
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
