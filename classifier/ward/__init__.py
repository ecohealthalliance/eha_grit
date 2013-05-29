from classifier import sklearn_cluster

from sklearn.cluster import Ward

def classify(train, test):
    clusterer = Ward(n_clusters=10)
    return sklearn_cluster.classify(train, test, clusterer)
