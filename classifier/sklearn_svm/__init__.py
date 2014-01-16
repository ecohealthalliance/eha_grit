from classifier import sklearn_classifier

from sklearn.svm import SVC

def train(train):
    svc = SVC(kernel='linear')
    return sklearn_classifier.train(train, svc)

def classify(test, model):
    return sklearn_classifier.classify(test, model)
