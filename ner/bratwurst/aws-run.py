import sys
sys.path.insert(0, '/var/www/bratwurst')

from bratwurst.application import application

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
