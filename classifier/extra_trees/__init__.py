from classifier import sklearn_classifier

from sklearn.ensemble import ExtraTreesClassifier

def classify(train, test):
    et = ExtraTreesClassifier()
    return sklearn_classifier.classify(train, test, et)
