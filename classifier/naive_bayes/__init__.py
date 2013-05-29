from classifier import sklearn_classifier

from sklearn.naive_bayes import MultinomialNB as NaiveBayes

def classify(train, test):
    nb = NaiveBayes()
    return sklearn_classifier.classify(train, test, nb)
