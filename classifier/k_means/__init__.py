from classifier import sklearn_cluster

from sklearn.cluster import KMeans

def classify(train, test):
    clusterer = KMeans()
    return sklearn_cluster.classify(train, test, clusterer)


    
