from flask import Flask, render_template, request
app = Flask(__name__)

# NOTE: IDs are used by the Disqus plug-in to distinguish betwixt pages.
# NOTE: When updating with a new blog post:
# 	1. Create a new host method for it. Iterate the id.
#	2. Update the Blog link in frame.html to point to the most recent post.
#	3. Update the previously most recent Blog post to point to the new post as the new most recent one.
#	   These URLs are generated within Jinja2 using eg. href='{{request.url_root}}2015/10/31/this-website.html'.

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

if __name__ == '__main__':
    app.run()
    # app.run(debug=True)