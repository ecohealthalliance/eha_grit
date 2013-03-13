from sys import argv 
import math
from svmutil import svm_problem, svm_parameter, svm_train, svm_predict

from io import read_table

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

'''def name2label (label, pos_name):
    if label == pos_name:
        return 1
    else:
        return -1'''

if __name__ == '__main__':
    data = read_table (argv[1])
    #test = read_table (argv[2])

    kernel = int (argv[2])

    for i in range (0, len (data)):
        train = []
        test = []
        for j, item in enumerate (data):
            if i != j:
                train.append (item)
            else:
                test.append (item)

        y = []
        x = []
        for item in train:
            #y.append (name2label (item['attr']['Disease'], label_name))
            y.append (label2int (item['attr']['Disease']))
            x.append (item['pos'])

        prob = svm_problem (y, x)
        param = svm_parameter ('-b 1 -q -t %d' % (kernel,))

        model = svm_train (prob, param)
        
        y = []
        x = []
        for item in test:
            #y.append (name2label (item['attr']['Disease'], label_name))
            y.append (label2int (item['attr']['Disease']))
            x.append (item['pos'])

        pred, accuracy, probabilities = svm_predict (y, x, model, '-b 1 -q')

        #if int (pred[0]) == name2label (test[0]['attr']['Disease'], label_name):
        test_label = test[0]['attr']['Disease']
        if accuracy[0] == 100:
            correct[test_label] += 1
            #print "Correctly classified %s in row %d with mse %d" % (test_label, i, accuracy[1])
            #print "Probabilities: %s" % ["%s: %f" % (int2label(i), probabilities[0][i]) for i in range(len(probabilities[0]))]
        else:
            print "Misclassified: %s as %s in row %d with mse %d" % (test_label, int2label (pred[0]), i, accuracy[1])
            print "Probabilties: %s: %f, %s: %f\n" % (test_label, probabilities[0][label2int(test_label)], int2label(pred[0]), probabilities[0][int(pred[0])])
            wrong[test_label] += 1
        
        #print test[0]['attr']['Disease'] + ' ' + str (name2label (test[0]['attr']['Disease'], label_name))  + ' ' + str (pred[0])

    print ''

    total_correct = 0
    total_wrong = 0

    for label in labels:
        print "%s identified %d/%d times (%d percent)" % (label, correct[label], correct[label] + wrong[label], int (round (float (correct[label]) / float (correct[label] + wrong[label]) * 100.00)))
        total_correct += correct[label]
        total_wrong += wrong[label]

    print ''
    print "Total Correct: %d/%d" % (total_correct, total_correct + total_wrong)
