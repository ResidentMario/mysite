from datetime import datetime
from flask import (Flask, render_template, abort, request, make_response, Response, send_from_directory, redirect, url_for)
from static.post_assets.citibike.citibike_trips import DataStore
import json
import os

app = Flask(__name__)
basepath = os.path.abspath(".")

# # Initialize the MongoDB connection (for CitiBike).
# db = DataStore(json.load(open(basepath + "/static/post_assets/citibike/mlab_instance_api_key.json"))['uri'])  # mLab

post_list = [
    {
        'title': 'An exercise in probability',
        'route': '2015/11/06/an-exercise-in-probability.html',
        'template': 'an-exercise-in-probability.html',
        'type': 'technical'
    },
    {
        'title': 'Measuring Wikipedia Signpost popularity',
        'route': '2016/01/17/signpost-views.html',
        'template': 'signpost-views.html',
        'type': 'exploration'
    },
    {
        'title': 'The decision to launch the Space Shuttle Challenger',
        'route': '2016/02/07/space-shuttle-challenger.html',
        'template': 'space-shuttle-challenger.html',
        'type': 'exploration'
    },
    {
        'title': 'Is Starbucks really always two blocks away?',
        'route': '2016/02/09/average-chain-distance.html',
        'template': 'average-chain-distance.html',
        'type': 'exploration'
    },
    {
        'title': 'Exploring the IBM Watson Concept Insights service using watsongraph',
        'route': '2016/02/11/watsongraph-visualization.html',
        'template': 'watsongraph-visualization.html',
        'type': 'exploration'
    },
    {
        'title': 'Analyzing WikiProjects on Wikipedia',
        'route': '2016/02/15/wikiprojects.html',
        'template': 'wikiprojects.html',
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
        'type': 'exploration'
    },
    {
        'title': 'Who are the biggest landowners in New York City?',
        'route': '2016/05/27/biggest-landowners-nyc.html',
        'template': 'biggest-landowners-nyc.html',
        'type': 'exploration'
    },
    {
        'title': 'Addressing in New York City',
        'route': '2016/06/01/nyc-addresses.html',
        'template': 'nyc-addresses.html',
        'type': 'exploration'
    },
    {
        'title': 'Residential property sales in New York City',
        'route': '2016/06/03/residential-property-sales.html',
        'template': 'residential-property-sales.html',
        'type': 'exploration'
    },
    {
        'title': 'Counting New York City street trees',
        'route': '2016/06/04/new-york-city-tree-density.html',
        'template': 'new-york-city-tree-density.html',
        'type': 'exploration'
    },
    {
        'title': 'Null and missing data in Python',
        'route': '2016/06/12/null-and-missing-data-python.html',
        'template': 'null-and-missing-data-python.html',
        'type': 'advocacy'
    },
    {
        'title': 'What are the most popular random seeds?',
        'route': '2016/07/08/randomly-popular.html',
        'template': 'randomly-popular.html',
        'type': 'technical'
    },
    {
        'title': 'The anatomy of an open data portal',
        'route': '2016/08/11/nyc-open-data-portal.html',
        'template': 'nyc-open-data-portal.html',
        'type': 'exploration'
    },
    {
        'title': 'The making of Life of Citi Bike',
        'route': '2016/08/27/day-in-the-life-of-citibike.html',
        'template': 'day-in-the-life-of-citibike.html',
        'type': 'technical'
    },
    {
        'title': 'Mapping Citi Bike routes',
        'route': '2016/09/14/citibike-map.html',
        'template': 'citibike-map.html',
        'type': 'exploration'
    },
    {
        'title': 'Saving progress in pandas',
        'route': '2016/10/29/saving-progress-pandas.html',
        'template': 'saving-progress-pandas.html',
        'type': 'technical'
    },
    {
        'title': 'In context: phase 2 of the Second Avenue Subway',
        'route': '2017/01/12/second-avenue-subway.html',
        'template': 'second-avenue-subway.html',
        'type': 'exploration'
    },
    {
        'title': 'Two million calls to 311',
        'route': '2017/02/13/311.html',
        'template': '311.html',
        'type': 'exploration'
    },
    {
        'title': 'Parsing subway rides with gtfs-tripify',
        'route': '2018/01/29/gtfs-tripify.html',
        'template': 'gtfs-tripify.html',
        'type': 'technical'
    },
    {
        'title': 'Kaggle kernels are Turing complete',
        'route': '2018/02/25/kaggle-kernels-are-turing-complete.html',
        'template': 'kaggle-kernels-are-turing-complete.html',
        'type': 'technical'
    },
    {
        'title': 'Designing data visualization APIs',
        'route': '2018/05/30/dataviz-apis.html',
        'template': 'dataviz-apis.html',
        'type': 'technical'
    },
    {
        'title': 'Tennis\'s wooden spoons',
        'route': '2018/06/10/tennis-wooden-spoons.html',
        'template': '/tennis-wooden-spoons.html',
        'type': 'exploration'
    },
    {
        'title': 'What next for open data?',
        'route': '2018/06/17/what-next-for-open-data.html',
        'template': '/what-next-for-open-data.html',
        'type': 'advocacy'
    },
    {
        'title': 'My approach to solving coding challenges',
        'route': '2018/08/14/solving-algorithms.html',
        'template': '/solving-algorithms.html',
        'type': 'technical'
    },
    {
        'title': 'Finding a model for collaboration in govtech that works',
        'route': '2018/08/19/finding-a-model-for-collaboration.html',
        'template': '/finding-a-model-for-collaboration.html',
        'type': 'advocacy'
    },
    {
        'title': 'Building an MTA historical train arrival application',
        'route': '2018/08/29/subway-explorer.html',
        'template': 'subway-explorer.html',
        'type': 'technical'
    },
    {
        'title': 'The three kinds of data scientists',
        'route': '2018/10/18/roles-in-data-science.html',
        'template': 'roles-in-data-science.html',
        'type': 'advocacy'
    },
    {
        'title': 'One year of taking notes with Jupyter on the cloud',
        'route': '2019/01/01/taking-notes-on-the-cloud.html',
        'template': 'taking-notes-on-the-cloud.html',
        'type': 'advocacy'
    },
    {
        'title': 'Mapping Ford Go Bike trips in the Bay Area',
        'route': '2019/01/15/ford-go-bike-maps.html',
        'template': 'ford-go-bike-maps.html',
        'type': 'exploration'
    },
    {
        'title': 'To be a more effective data scientist, think in experiments',
        'route': '2019/02/23/data-science-experiments.html',
    },
    {
        'title': 'Making Python classes more modular using mixins',
        'route': '2019/07/07/python-mixins.html',
        'template': 'python-mixins.html',
        'type': 'technical'
    },
    {
        'title': 'Bringing together building, block, street, and point data',
        'route': '2019/08/03/buildings-blocks-streets-points.html',
        'template': 'buildings-blocks-streets-points.html',
        'type': 'technical',
        'date': '2019/08/03'
    },
]

post_paths = [post['route'] for post in post_list]

project_list = [
    {
        'title': 'missingno',
        'subtitle': 'A missing data visualization library',
        'snap': 'missingno.png',
        'route': '2016/03/28/missingno.html',
        'template': 'missingno.html',
    },
    {
        'title': 'py_d3',
        'subtitle': 'D3.JS in Jupyter',
        'snap': 'py-d3.png',
        'route': '2016/09/12/py-d3.html',
        'template': 'py-d3.html',
    },
    {
        'title': 'life of citibike',
        'subtitle': 'Visualizing a day of trips on Citi Bike',
        'snap': 'life-of-citibike.png',
        'route': '2016/08/27citibike-project.html',
        'template': 'citibike.html'
    },
    {
        'title': 'geoplot',
        'subtitle': 'High-level geospatial plotting',
        'snap': 'geoplot.png',
        'route': '2017/02/07/geoplot.html',
        'template': 'geoplot.html',
    },
    {
        'title': 'two million calls to 311',
        'subtitle': 'A hierarchical treemap',
        'snap': '311.png',
        'route': '2017/02/13/311-threshold-tree.html',
        'template': '311-threshold-tree.html'
    },
    # {
    #     'title': 'airscooter',
    #     'subtitle': 'A wide-data management tool',
    #     'snap': 'missingno.png',
    #     'route': '2017/08/22/airscooter.html',
    #     'template': 'airscooter.html'
    # },
    {
        'title': 'gtfs-tripify',
        'subtitle': 'GTFS-RT train arrival time parser',
        'snap': 'gtfs-tripify.png',
        'route': '2018/01/29/gtfs-tripify-parser.html',
        'template': 'gtfs-tripify-parser.html',
    },
    {
        'title': 'kaggle learn',
        'subtitle': 'Coursework on data analysis and data viz',
        'snap': 'kaggle-learn.png',
        'route': '2018/10/19/kaggle-learn.html',
        'template': 'kaggle-learn.html'
    },
    {
        'title': 'machine learning notes',
        'subtitle': 'Notes on machine learning',
        'snap': 'ml-notes.png',
        'route': '2018/09/04/machine-learning-notes.html',
        'template': 'machine-learning-notes.html'
    },
    {
        'title': 'fahr',
        'subtitle': 'Remote machine learning training',
        'snap': 'fahr.png',
        'route': '2019/01/22/fahr.html',
        'template': 'fahr.html'
    },
    {
        'title': 'rubbish story',
        'subtitle': 'Visualizing San Francisco street trash',
        'snap': 'rubbish-story.png',
        'route': '2019-09-11/rubbish-story.html',
        'template': 'rubbish-story.html'
    },
    {
        'title': 'paint with ml',
        'subtitle': 'Become a deep learning artist',
        'snap': 'paint-with-ml.png',
        'route': '2020-09-16/paint-with-ml.html',
        'template': 'paint-with-ml.html'
    },
    {
        'title': 'rubbish geo',
        'subtitle': 'A geospatial analytics service',
        'snap': 'rubbish-geo.png',
        'route': '2020-09-16/rubbish-geo.html',
        'template': 'rubbish-geo.html'
    },
    {
        'title': 'aleksey-writes',
        'subtitle': 'Search my 2016-2020 writings',
        'snap': 'aleksey-writes.png',
        'route': '2021-02-21/aleksey-writes.html',
        'template': 'aleksey-writes.html'
    }
][::-1]

project_paths = [project['route'] for project in project_list]

advocacy_list = [
    {
        'title': 'Who runs the world? Data',
        'route': 'https://www.amny.com/opinion/columnists/mark-chiusano/who-run-the-world-data-says-aleksey-bilogur-1.11863032',
        'date': '2016-06-01'
    },
    # {
    #     'title': 'Implementing good design',
    #     'route': 'https://www.meetup.com/NYC-D3-JS/events/234355571/',
    #     'date': '2016-09-26'
    # },
    # {
    #     'title': 'Becoming a civic technologist out of college',
    #     'route': 'https://blog.codingitforward.com/becoming-a-civic-technologist-out-of-college-4bcb37f9777c',
    #     'date': '2017-09-01'
    # },
    # {
    #     'title': 'Learning by doing with data viz blogging',
    #     'route': 'https://www.meetup.com/DataVisualization/events/245257327/',
    #     'date': '2017-12-12'
    # },
    # {
    #     'title': 'Profiling top Kagglers: Bestfitting, currently #1 in the world',
    #     'route': 'http://blog.kaggle.com/2018/05/07/profiling-top-kagglers-bestfitting-currently-1-in-the-world/',
    #     'date': '2018-05-07'
    # },
    {
        'title': 'Reproduce a machine learning model build in four lines of code',
        'route': 'https://blog.quiltdata.com/reproduce-a-machine-learning-model-build-in-four-lines-of-code-b4f0a5c5f8c8',
        'date': '2019-01-17'
    },
    {
        'title': 'Building fully custom machine learning models on AWS SageMaker: a practical guide',
        'route': 'https://towardsdatascience.com/building-fully-custom-machine-learning-models-on-aws-sagemaker-a-practical-guide-c30df3895ef7',
        'date': '2019-02-12'
    },
    {
        'title': 'How to classify photos in 600 classes using nine million Open Images',
        'route': 'https://www.freecodecamp.org/news/how-to-classify-photos-in-600-classes-using-nine-million-open-images-65847da1a319/',
        'date': '2019-02-20'
    },
    {
        'title': 'Import almost anything in Python: an intro to module loaders and finders',
        'route': 'https://blog.quiltdata.com/import-almost-anything-in-python-an-intro-to-module-loaders-and-finders-f5e7b15cda47',
        'date': '2019-03-04'
    },
    {
        'title': 'Evaluating Keras neural network performance using Yellowbrick visualizations',
        'route': 'https://towardsdatascience.com/evaluating-keras-neural-network-performance-using-yellowbrick-visualizations-ad65543f3174',
        'date': '2019-03-21'
    },
    {
        'title': 'Boost your CNN classifier performance with progressive resizing in Keras',
        'route': 'https://towardsdatascience.com/boost-your-cnn-image-classifier-performance-with-progressive-resizing-in-keras-a7d96da06e20',
        'date': '2019-04-01'
    },
    {
        'title': 'Building a fully reproducible machine learning pipeline with CometML and Quilt',
        'route': 'https://medium.com/comet-ml/building-a-fully-reproducible-machine-learning-pipeline-with-comet-ml-and-quilt-aa9c7bf85e72',
        'date': '2019-05-13'
    },
    {
        'title': 'François Chollet wants you to care about developer experience',
        'route': 'https://blog.quiltdata.com/fran%C3%A7ois-chollet-wants-you-to-care-about-developer-experience-5fd049e45642',
        'date': '2019-06-07'
    },
    {
        'title': 'Using Spark for model featurization with Spell',
        'route': 'https://spell.ml/blog/using-spark-for-model-featurization-with-spell-XnEedBUAACcAjfTV',
        'date': '2020-03-29'
    },
    {
        'title': 'An introduction to hyperparameter search with CIFAR10',
        'route': 'https://spell.ml/blog/an-introduction-to-hyperparameter-search-with-cifar10-Xo8_6BMAACEAkwVs',
        'date': '2020-04-13'
    },
    {
        'title': 'Automating GPU machine failure recovery in Google Compute Engine',
        'route': 'https://spell.ml/blog/automated-machine-failure-recovery-Xp3TEhEAACUAYwPM',
        'date': '2020-04-27'
    },
    {
        'title': 'Reduce cloud GPU model training costs by 66% using spot instances',
        'route': 'https://spell.ml/blog/reduce-gpu-model-training-costs-using-spot-XqtgJBAAACMAR6h8',
        'date': '2020-05-10'
    },
    {
        'title': 'It\'s 2020, why isn\'t deep learning 100% on the cloud yet?',
        'route': 'https://spell.ml/blog/deep-learning-infrastructure-in-2020-Xr2s7xEAACEAv28w',
        'date': '2020-05-17'
    },
    {
        'title': 'Battle-tested techniques for scoping machine learning projects',
        'route': 'https://github.com/spellrun/ml-project-scoping-talk',
        'date': '2020-06-11'
    },
    {
        'title': 'A developer-friendly guide to mixed-precision training with PyTorch',
        'route': 'https://spell.ml/blog/mixed-precision-training-with-pytorch-Xuk7YBEAACAASJam',
        'date': '2020-06-15'
    },
    {
        'title': 'Distributed model training in PyTorch using DistributedDataParallel',
        'route': 'https://spell.ml/blog/pytorch-distributed-data-parallel-XvEaABIAAB8Ars0e',
        'date': '2020-06-21'
    },
    {
        'title': 'Distributed model training using Horovod',
        'route': 'https://spell.ml/blog/distributed-model-training-using-horovod-XvqEGRUAACgAa5th',
        'date': '2020-06-29'
    },
    {
        'title': 'Getting started with large scale ETL jobs using Dask and AWS EMR',
        'route': 'https://spell.ml/blog/large-scale-etl-jobs-using-dask-Xyl8GhEAACQAjK6h',
        'date': '2020-08-03'
    },
    {
        'title': 'Getting oriented in the RAPIDS distributed ML ecosystem, part 1: ETL',
        'route': 'https://spell.ml/blog/getting-oriented-in-the-rapids-distributed-ml-ecosystem-part-1-X1gixBIAAJ7nyzHa',
        'date': '2020-09-12'
    },
    {
        'title': 'What does the machine learning workspace of the future look like?',
        'route': 'https://spell.ml/blog/the-learning-workspace-of-the-future-X1_MkRAAACMAXG0v',
        'date': '2020-09-14'
    },
    {
        'title': 'MLOps concepts for busy engineers: model serving',
        'route': 'https://spell.ml/blog/mlops-concepts-model-serving-X385lREAACcAAGzS',
        'date': '2020-10-07'
    },
    {
        'title': 'The key components of a successful MLOps strategy',
        'route': 'https://spell.ml/blog/components-of-an-mlops-strategy-X4d_KREAACUAvo6M',
        'date': '2020-10-14'
    },
    {
        'title': 'Getting oriented in the RAPIDS distributed ML ecosystem, part 2: training and scoring',
        'route': 'https://spell.ml/blog/getting-oriented-in-the-rapids-distributed-ml-ecosystem-part-2-X68AOxIAACAAacZk',
        'date': '2020-11-12'
    },
    {
        'title': 'A developer-friendly guide to model quantization with PyTorch',
        'route': 'https://spell.ml/blog/pytorch-quantization-X8e7wBAAACIAHPhT',
        'date': '2020-12-01'
    },
    {
        'title': 'A developer-friendly guide to model pruning with PyTorch',
        'route': 'https://spell.ml/blog/model-pruning-in-pytorch-X9pXQRAAACIAcH9h',
        'date': '2020-12-15'
    }
]


@app.route('/')
def main_page():
    return render_template('home.html', post_list=post_list)


@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/advocacy.html')
def advocacy():
    return render_template('advocacy.html', advocacy_list=advocacy_list)


@app.route('/portfolio.html')
def portfolio():
    return render_template('projects.html', project_list=project_list)


@app.route('/visualizations/<path:path>')
def display_visualization(path):
    return render_template('visualizations/' + path)


# @app.route('/citibike-api/<path:path>/id/<int:stationid>')
# def citibike_sample(path, stationid):
#     if path == 'bike-outbounds':
#         collection_name = 'outbound bike trip indices'
#     elif path == 'bike-inbounds':
#         collection_name = 'inbound bike trip indices'
#     elif path == 'outgoing-trips':
#         collection_name = 'outgoing trip indices'
#     elif path == 'incoming-trips':
#         collection_name = 'incoming trip indices'
#     else:
#         abort(404)
#         return
#     tripset = db.get_station_bikeset(stationid, collection_name)
#     # Remove None trips---these correspond with trips that have not been populated in the database yet!
#     tripset = [trip for trip in tripset if trip is not None]
#     return Response(json.dumps(tripset), mimetype='application/json')


@app.route('/<path:path>')
def serve(path):
    if path in post_paths:
        index = post_paths.index(path)
        post = post_list[index]
        date_str = post['route'][:10]
        year, month, day = date_str[:4], date_str[5:7], date_str[8:10]
        return render_template(
            'posts/' + post['template'],
            id=index + 1,
            date="{0}/{1}/{2}".format(month, day, year),
            title=post['title']
        )
    elif path in project_paths:
        index = project_paths.index(path)
        project = project_list[index]
        date_str = project['route'][:10]
        year, month, day = date_str[:4], date_str[5:7], date_str[8:10]
        return render_template(
            'projects/' + project['template'],
            id=index + 1,
            date="{0}/{1}/{2}".format(month, day, year),
            title=project['title']
        )
    else:
        abort(404)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
