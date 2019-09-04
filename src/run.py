__author__ = 'salton'
from src.app import app

# website starter
app.run(debug=app.config['DEBUG'], port=4990)
