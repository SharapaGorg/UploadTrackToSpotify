from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/spotipy/')
def redirect(var):
    # print(var, file = open('.log', 'w'))
    
    return 'DEATh'

app.run(debug=True)