from classifier import sklearn_classifier

from sklearn.ensemble import RandomForestClassifier

def classify(train, test):
    rf = RandomForestClassifier()
    return sklearn_classifier.classify(train, test, rf)
