import flask

app = flask.Flask(__name__)

list_of_data = [1, 3, 4]


@app.route('/')
def index():
    # response = "hello, world\n"
    # response += '<a href="' + flask.url_for('temperature') + '">Temperature</a>'
    # response += '<button type="button">up</button>'
    # response += '<button type="button">down</button>'

    global list_of_data
    response = list_of_data[0]

    response = str(response)
    return response
	
@app.route('/temp_data')
def temperature():
	
	return '75'





app.debug = True

app.run( 
        host="10.18.8.5",
        port=int("5000")
  )