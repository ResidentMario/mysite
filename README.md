Between the data analysis projects that I run through and the software libraries that I tinker with, I write a lot of
 code. My personal website helps me keep track of things by giving me a space in which to ruminate on what I've
 done, where I'm going, and how I'm going to get there.

The service is written in [Flask](http://flask.pocoo.org/) and hosted on [PythonAnywhere](https://www.pythonanywhere.com). Content is written in HTML and CSS, with templating via [Jinja2](http://jinja.pocoo.org/docs/dev/).

Current worflow:
1. Add the new post to `post_list` in `app.py`.
2. Run `munge_posts.py` (this generates the RSS Feed).
3. `git push`
4. `git pull` on PythonAnywhere.
5. Reload.
