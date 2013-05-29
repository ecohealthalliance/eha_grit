from classifier import sklearn_cluster

from sklearn.mixture import GMM

def classify(train, test):
    clusterer = GMM()
    return sklearn_cluster.classify(train, test, clusterer)

    
    
