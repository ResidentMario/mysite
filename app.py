from flask import Flask
from flask import render_template
from flask import redirect

app = Flask(__name__)


# NOTE: IDs are used by the Disqus plug-in to distinguish betwixt pages.
# NOTE: When updating with a new blog post:
# 1. Create a new host method for it. Iterate the id.
# 2. Update the Blog link in frame.html to point to the most recent post.
# 3. Update the previously most recent Blog post to point to the new post as the new most recent one.
# These URLs are generated within Jinja2 using eg. href='{{request.url_root}}2015/10/31/this-website.html'.

# TODO: Automagically host blog posts using a list of posts and an iterative generator (url_for).
# TODO: Automagically host summaries of recent blog posts on the About page (using the same technique).

@app.route('/')
def home():
    return render_template('about.html')


@app.route('/2015/11/06/an-exercise-in-probability.html')
def first_post():
    return render_template('an_exercise_in_probability.html', id=1)


@app.route('/2015/10/31/this-website.html')
def second_post():
    return render_template('this_website.html', id=2)


@app.route('/2015/12/12/openness-versus-quality.html')
def third_post():
    return render_template('openness_versus_quality.html', id=3)


@app.route('/2015/12/26/watson.html')
def fourth_post():
    return render_template('watson.html', id=4)


@app.route('/2016/01/17/signpost-views.html')
def fifth_post():
    return render_template('signpost_views.html', id=5)


@app.route('/2016/02/07/space-shuttle-challenger.html')
def sixth_post():
    return render_template('challenger.html', id=6)


@app.route('/2016/02/09/average-chain-distance.html')
def average_chain_distance():
    return render_template('average_chain_distance.html', id=7)


@app.route('/2016/02/11/watsongraph-visualization.html')
def watsongraph_visualization():
    return render_template('watsongraph_visualization.html', id=8)

@app.route('/2016/02/15/wikiprojects.html')
def wikiprojects():
    return render_template('wikiprojects.html', id=9)

# RAW HOSTING
@app.route('/raw/challenger-compact.html')
def challenger_compact():
    return render_template('raw_challenger_compact.html')


@app.route('/raw/challenger-extended.html')
def challenger_extended():
    return render_template('raw_challenger_extended.html')


@app.route('/raw/gregorys-map.html')
def gregorys_map():
    return render_template('raw_gregorys_map.html')


@app.route('/raw/dunkin-donuts-map.html')
def dunkin_map():
    return render_template('raw_dunkin_donuts_map.html')


@app.route('/raw/starbucks-map.html')
def starbucks_map():
    return render_template('raw_starbucks_map.html')


@app.route('/raw/manhattan-point-cloud.html')
def manhattan_point_cloud():
    return render_template('manhattan_point_cloud.html')


@app.route('/raw/average-chain-distance-viz.html')
def average_chain_distance_viz():
    return render_template('average_chain_distance_viz.html')


@app.route('/raw/contributions-visualization.html')
def raw_contributions():
    return render_template('raw_contributions_visualization.html')


@app.route('/raw/fortune-visualization.html')
def raw_fortune():
    return render_template('raw_fortune_visualization.html')


@app.route('/raw/planets-visualization.html')
def raw_planets():
    return render_template('raw_planets_visualization.html')


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)
