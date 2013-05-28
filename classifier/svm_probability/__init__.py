from sys import argv 
import math
from svmutil import svm_problem, svm_parameter, svm_train, svm_predict

def classify (train, test, kernel=0):

    diseases = set([row['attr']['Disease'] for row in train])

    test_label = test[0]['attr']['Disease']
    disease_probabilities = [dict((disease, 0) for disease in diseases) for _ in range(0, len(test))]

    for disease in diseases:

        y = []
        x = []
        for item in train:
            if item['attr']['Disease'] == disease:
                y.append(0)
            else:
                y.append(1)
            x.append(item['pos'])


        prob = svm_problem (y, x)
        param = svm_parameter ('-b 1 -q -t %d' % (kernel,))

        model = svm_train (prob, param)
        
        y = []
        x = []
        for item in test:
            if item['attr']['Disease'] == disease:
                y.append(0)
            else:
                y.append(1)
            x.append(item['pos'])

        pred, accuracy, probabilities = svm_predict (y, x, model, '-b 1 -q')

        first_label = (train[0]['attr']['Disease'] == disease)
        for i in range(0, len(test)):
            if first_label:
                disease_probabilities[i][disease] = probabilities[i][0]
            else:
                disease_probabilities[i][disease] = probabilities[i][1]

    predictions = [max(disease_probabilities[i].iterkeys(), key=(lambda key: disease_probabilities[i][key])) for i in range(0, len(test))]
    return (predictions, disease_probabilities)


