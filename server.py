import flask
from flask import render_template, request
from run import test
from classifiers import sklearn_svm

app = flask.Flask(__name__)

@app.route('/diagnose', methods = ['POST'])
def diagnose():
	training_data = request.form['training_data']
	test_data = request.form['test_data']
	print training_data
	print test_data
	print test(training_data, test_data, sklearn_svm)



app.run(debug = True)