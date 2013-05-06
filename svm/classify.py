from sys import argv 
import math
from svmutil import svm_problem, svm_parameter, svm_train, svm_predict

from io import read_table


if __name__ == '__main__':
    data = read_table (argv[1])
    #test = read_table (argv[2])

    kernel = int (argv[2])

    diseases = set([row['attr']['Disease'] for row in data])
    correct = dict((disease, 0) for disease in diseases)
    wrong = dict((disease, 0) for disease in diseases)

    for i in range (0, len (data)):
        test_label = data[i]['attr']['Disease']

        disease_probabilities = dict((disease, 0) for disease in diseases)

        for disease in diseases:
            test = [data[i]]
            train = [row for j, row in enumerate(data) if j != i]

            y = []
            x = []
            for item in train:
                if item['attr']['Disease'] == disease:
                    y.append(0)
                else:
                    y.append(1)
                x.append (item['pos'])

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
                x.append (item['pos'])

            pred, accuracy, probabilities = svm_predict (y, x, model, '-b 1 -q')
            #prob_disease = probabilities[0][0]
            #prob_not_disease = probabilities[0][1]
            #print "testing %s for not %s/%s" % (test_label, disease, disease)
            #print "predicted %s" % (disease if pred[0] == 0 else "not %s" % disease)
            #print "%s / %s / %s" % (pred, accuracy, probabilities)
            #print
            #print "prob: %s- %f, %s- %f" % (disease, prob_disease, "not %s" % disease, prob_not_disease)
            disease_probabilities[disease] = min(probabilities[0]) if accuracy[0] == 100 else max(probabilities[0])
            #if disease_probabilities[disease] > 0.5 and test_label == disease:
            #    correct[test_label] += 1
            #elif disease_probabilities[disease] < 0.5 and test_label != disease:
            #    correct[test_label] += 1
            #else:
            #    wrong[test_label] += 1
            #    print "Misclassified %s as %s in row %d" % (test_label, disease if test_label != disease else "not %s" % disease, i)
            #print

        prediction = max(disease_probabilities.iterkeys(), key=(lambda key: disease_probabilities[key]))
        if prediction == test_label:
            correct[test_label] += 1
        else:
            wrong[test_label] += 1
            print "Misclassified: %s as %s in row %d" % (test_label, prediction, i)
            print "Probabilties: %s\n" % disease_probabilities

        
        #print test[0]['attr']['Disease'] + ' ' + str (name2label (test[0]['attr']['Disease'], label_name))  + ' ' + str (pred[0])

    print ''

    total_correct = 0
    total_wrong = 0

    for label in diseases:
        print "%s identified %d/%d times (%d percent)" % (label, correct[label], correct[label] + wrong[label], int (round (float (correct[label]) / float (correct[label] + wrong[label]) * 100.00)))
        total_correct += correct[label]
        total_wrong += wrong[label]

    print ''
    print "Total Correct: %d/%d" % (total_correct, total_correct + total_wrong)
