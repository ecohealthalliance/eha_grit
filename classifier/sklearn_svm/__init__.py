from classifier import sklearn_classifier

from sklearn.svm import SVC

def classify(train, test):
    svc = SVC(kernel='linear')
    return sklearn_classifier.classify(train, test, svc)
