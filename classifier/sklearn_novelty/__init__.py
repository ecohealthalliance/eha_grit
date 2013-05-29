from sklearn.svm import OneClassSVM

def classify(train, test):

    x = []
    for item in train:
        x.append(item['pos'])

    classifier = OneClassSVM(nu=0.1, kernel='linear', gamma=0.1)
    classifier.fit(x)

    x = []
    for item in test:
        x.append(item['pos'])

    pred = classifier.predict(x)
    results = []
    for prediction in pred:
        if prediction == 1:
            results.append('Regular')
        else:
            results.append('Novel')
    return (results, [{} for i in range(0, len(test))])
