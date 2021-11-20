from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/spotipy/')
def redirect():
    
    return 'DEATh'

app.run(debug=True)