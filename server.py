try:
    import sys
    sys.path.insert(0, '/var/lib/jenkins/jobs/diagnose-deploy/workspace')

    import flask
    from flask import render_template, request
    from run import test, train as train_model
    from classifier import sklearn_svm
    import json

    app = flask.Flask(__name__)

    all_symptoms = []
    trained_svm = None

    @app.route('/status', methods= ['GET'])
    def status():
        return "true"

    @app.route('/train', methods = ['POST'])
    def train():
        global all_symptoms, trained_svm
        data = json.loads(request.data)
        training_data = data.get('training_data')
        all_symptoms = set([])
        for report in training_data:
            all_symptoms = all_symptoms.union(report.get('symptoms'))
        all_symptoms = list(all_symptoms)
        training_nodes = []
        id = 0
        for report in training_data:
            attr = {'Disease': report.get('disease'), 'ID': id}
            pos = []
            for symptom in all_symptoms:
                val = 0
                if symptom in report.get('symptoms'):
                    val = 1
                attr[symptom] = val
                pos.append(val)
            item = {
                '_id': id,
                'pos': pos,
                'attr': attr,
            }
            training_nodes.append(item)
            id += 1
        trained_svm = train_model(training_nodes, sklearn_svm)
        return 'true'

    @app.route('/diagnose', methods = ['POST'])
    def diagnose():
        global all_symptoms, trained_svm
        data = json.loads(request.data)
        test_data = data.get('test_data')
        pos = []
        attr = {'Disease': 'unknown', 'ID': 0}
        for symptom in all_symptoms:
            val = 0
            if symptom in test_data:
                val = 1
            pos.append(val)
            attr[symptom] = val
        test_node = {'pos': pos, 'attr': attr,  '_id': 0, 'ID': 0}
        print trained_svm
        prediction = test([test_node], trained_svm, sklearn_svm)[0]
        return prediction
    

    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)

except Exception, ex:
    import sys
    from traceback import format_list, extract_tb
    (extype, value, trace) = sys.exc_info()
    print >> sys.stderr, "%s:%s\n%s" % (extype, value, ''.join(format_list(extract_tb(trace))))
