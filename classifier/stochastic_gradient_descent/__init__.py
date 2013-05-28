from classifier import sklearn_classifier

from sklearn.linear_model import SGDClassifier

def classify(train, test):
    sgd = SGDClassifier()
    return sklearn_classifier.classify(train, test, sgd)
