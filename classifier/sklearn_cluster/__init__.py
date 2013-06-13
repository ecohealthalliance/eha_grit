import numpy as np

def classify(train, test, clusterer):

    y = []
    x = []
    for item in train:
        x.append (item['pos'])
    for item in test:
        x.append (item['pos'])

    clusterer.fit(x)

    if hasattr(clusterer, 'predict'):
        results = clusterer.predict(x)
    else:
        results = clusterer.labels_

    train_clusters = results[0:len(train)]
    test_clusters = results[len(train):]

    test_predictions = []
    for i in range(0, len(test)):
        cluster = test_clusters[i]
        matches = [train[index] for index in range(0, len(train)) if train_clusters[index] == cluster]
        diseases = [item['attr']['Disease'] for item in matches]
        disease_counts = {name: diseases.count(name) for name in np.unique(diseases)}
        test_predictions.append(max(disease_counts.iterkeys(), key=(lambda key: disease_counts[key])))
    return (test_predictions, [{} for i in range(0, len(test))])

    
