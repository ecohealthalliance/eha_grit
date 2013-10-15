import argparse
from collections import defaultdict
from importlib import import_module

from format import bogich

FORMATS = {
    'bogich': bogich,
}

CLASSIFIERS = [
    'sklearn_svm',
    'naive_bayes',
    'decision_tree',
    'stochastic_gradient_descent',
    'random_forest',
    'gradient_boosting',
    'extra_trees',
    'gmm',
    'k_means',
    'ward',
    'sklearn_novelty',
    'matrix',
]

def cross_validate(data, classifier):
    correct = defaultdict(int)
    wrong = defaultdict(int)

    for i in range(0, len(data)):
        train = []
        test = []
        for j, item in enumerate(data):
            if i != j:
                train.append(item)
            else:
                test.append(item)

        disease_map = {
            'Bacterial Meningitis' : 'Meningitis-bacterial',
            'Dengue' : 'Dengue',
            'JE' : 'Japanese Encephalitis',
            'Measles' : 'Measles',
            'Malaria' : 'Malaria',
            'Meningitis-aseptic' : 'Meningitis -aseptic (viral)',
            'Nipah Virus' : 'Nipah and Nipah-like Virus Disease',
            'Typhoid/Enteric Fever' : 'Typhoid and Enteric Fever',
            'Chandipura' : 'Chandipura and Vesicular stomatitis viruses',
            'Chikungunya' : 'Chikungunya',
        }

        (predictions, probabilities) = classifier.classify(train, test)
        prediction = predictions[0]
        actual = test[0]['attr']['Disease']
        if prediction == disease_map.get(actual):
            correct[actual] += 1
        else:
            print "Misclassified %s as %s in row %d" % (actual, prediction, i)
            print "Symptoms for %s: %s" % (disease_map.get(actual), probabilities[0].get(disease_map.get(actual)))
            print "Symptoms for %s: %s" % (prediction, probabilities[0].get(prediction))
            print
            wrong[actual] += 1

    total_correct = 0
    total_wrong = 0

    for label in set(correct.keys() + wrong.keys()):
        print "%s identified %d/%d times (%d percent)" % (label, correct[label], correct[label] + wrong[label], int (round (float (correct[label]) / float (correct[label] + wrong[label]) * 100.00)))
        total_correct += correct[label]
        total_wrong += wrong[label]

    print ''
    print "Total Correct: %d/%d" % (total_correct, total_correct + total_wrong)

def test(train, test, classifier):
    correct = defaultdict(int)
    wrong = defaultdict(int)

    (predictions, probabilities) = classifier.classify(train, test)

    for i in range(0, len(test)):
        actual = test[i]['attr']['Disease']
        if actual:
            if actual == predictions[i]:
                correct[actual] += 1
            else:
                print "Misclassified %s as %s" % (actual, predictions[i])
                wrong[actual] += 1

    total_correct = 0
    total_wrong = 0

    for label in set(correct.keys() + wrong.keys()):
        print "%s identified %d/%d times (%d percent)" % (label, correct[label], correct[label] + wrong[label], int (round (float (correct[label]) / float (correct[label] + wrong[label]) * 100.00)))
        total_correct += correct[label]
        total_wrong += wrong[label]

    print ''
    print "Total Correct: %d/%d" % (total_correct, total_correct + total_wrong)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Train classifiers and run on test datas.')
    
    parser.add_argument('-training', help="Training data file", default="ProMED_master_clean.csv")
    parser.add_argument('-training_format', help="Format of training data", choices=FORMATS.keys(), default="bogich")
    parser.add_argument('-classifier', help="Classifier", choices=CLASSIFIERS, default='svm_standard')
    parser.add_argument('-cross_validate', help="Whether to run cross validation", default=False)
    parser.add_argument('-test', help="Test data file", default=None)
    parser.add_argument('-test_format', help="Format of test data", choices=FORMATS.keys(), default="bogich")

    args = parser.parse_args()

    training_format = FORMATS[args.training_format]

    training_data = training_format.read(args.training)

    classifier = import_module("classifier.%s" % args.classifier)

    if args.cross_validate:
        print "Running cross validation"
        cross_validate(training_data, classifier)

    if args.test:
        print "Testing"
        
        test_format = FORMATS[args.test_format]

        test_data = test_format.read(args.test)

        test(training_data, test_data, classifier)

