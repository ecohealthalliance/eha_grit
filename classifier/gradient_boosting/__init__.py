from classifier import sklearn_classifier

from sklearn.ensemble import GradientBoostingClassifier

def classify(train, test):
    gb = GradientBoostingClassifier()
    return sklearn_classifier.classify(train, test, gb)
