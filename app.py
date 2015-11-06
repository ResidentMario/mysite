from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('about.html')

@app.route('/2015/09/31/an-exercise-in-probability.html')
def first_post():
    return render_template('an_exercise_in_probability.html')

@app.route('/blog/an-exercise-in-linear-algebra')
def second_post():
    return render_template('second_post.html')

if __name__ == '__main__':
    app.run(debug=True)