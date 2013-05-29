from classifier import sklearn_classifier

from sklearn.tree import DecisionTreeClassifier

def classify(train, test):
    tree = DecisionTreeClassifier()
    return sklearn_classifier.classify(train, test, tree)
