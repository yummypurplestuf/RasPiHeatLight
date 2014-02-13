import flask, flask.views

app = flask.Flask(__name__)



class View(flask.views.MethodView):
	def get(self):
		return flask.render_template('index.html')

app.add_url_rule('/', view_func=View.as_view('main'))












app.debug = True

app.run()