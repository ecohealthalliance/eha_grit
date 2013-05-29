from sys import argv 
import math
from svmutil import svm_problem, svm_parameter, svm_train, svm_predict

max_label = 0
labels = {}
inv_labels = {}

correct = {}
wrong = {}

def label2int (label):
    global max_label, labels, inv_labels, correct, wrong
    if not labels.has_key (label):
        labels[label] = max_label
        inv_labels[max_label] = label
        max_label += 1
        correct[label] = 0
        wrong[label] = 0
    return labels[label]

def int2label (label_int):
    global max_label, labels, inv_labels
    return inv_labels[label_int]


def classify (train, test, kernel=0):

    y = []
    x = []
    for item in train:
        y.append (label2int (item['attr']['Disease']))
        x.append (item['pos'])

    prob = svm_problem (y, x)
    param = svm_parameter ('-q -t %d' % (kernel,))

    model = svm_train (prob, param)
        
    y = []
    x = []
    for item in test:
        y.append (label2int (item['attr']['Disease']))
        x.append (item['pos'])

    pred = svm_predict (y, x, model, '-q')
    return ([int2label(prediction) for prediction in pred[0]], [{} for i in range(0, len(test))])

