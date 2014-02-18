import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    response = "hello, world\n"
    response += '<a href="' + flask.url_for('temperature') + '">Temperature</a>'
    response += '<button type="button">up</button>'
    response += '<button type="button">down</button>'
    
    return response
	
@app.route('/temp_data')
def temperature():
	
	return '75'





app.debug = True

app.run()