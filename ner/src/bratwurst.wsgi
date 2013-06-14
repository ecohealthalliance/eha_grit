import sys
sys.path.insert(0, '/var/www/bratwurst')

from app import app
app.run(debug = True)