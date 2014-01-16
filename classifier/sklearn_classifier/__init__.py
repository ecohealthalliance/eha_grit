
max_label = 0
labels = {}
inv_labels = {}

correct = {}
wrong = {}

def label2int (label):
    global max_label, labels, inv_labels, correct, wrong
    if not labels.has_key (label):
        labels[label] = max_label
        inv_labels[max_label] = label
        max_label += 1
        correct[label] = 0
        wrong[label] = 0
    return labels[label]

def int2label (label_int):
    global max_label, labels, inv_labels
    return inv_labels[label_int]


def train(train, classifier):
    y = []
    x = []
    for item in train:
        y.append (label2int(item['attr']['Disease']))
        x.append (item['pos'])

    model = classifier.fit(x, y)
    return model

def classify(test, model):
    x = []
    for item in test:
        x.append(item['pos'])
    return ([int2label(prediction) for prediction in model.predict(x)], [{} for i in range(0, len(test))])
