from flask import render_template, request
from bratwurst.application import application as app
from glob import glob
import re
import json
from os import system

@app.route('/')
@app.route('/index')
def index():
    PATH = app.config['BRAT_DATA_LOCATION']
    files = glob("%s*.txt" % PATH)
    ids = [file.split("/")[-1].split(".")[0] for file in files]
    annotated_ids = []
    for id in ids:
        with open('%s%s.ann' % (PATH, id)) as f:
            ann = f.read()
            if ann:
                annotated_ids.append(id)
                      
    return render_template("index.html",
        ids = ids, annotated_ids = annotated_ids, brat_url = app.config['BRAT_URL'])

@app.route('/train')
def train():
    PATH = app.config['BRAT_DATA_LOCATION']
    annotation_files = glob("%s*.ann" % PATH)
    training_data = ""

    for file in annotation_files:
        id = file.split("/")[-1].split(".")[0]
        with open(file) as ann_file:
            ann = ann_file.read()

            if ann:
                annotations = dict()
                for annotation in ann.split('\n'):
                    ann_parts = annotation.replace('\t', ' ').split(' ')
                    if (len(ann_parts) >= 4):
                        next_ann_start = int(ann_parts[2])
                        annotations[next_ann_start] = ann_parts


                with open(file.replace('ann', 'txt')) as txt_file:
                    txt = txt_file.read()

                    type = 'other'
                    word = ''
                    for i in range(0, len(txt)):
                        next_char = txt[i]

                        if annotations.get(i):
                            type = annotations[i][1]

                        if re.compile('\s').match(next_char) and len(word):
                            training_data += '%s %s\n' % (word, type)
                            word = ''
                            type = 'other'
                        elif not re.compile('\s').match(next_char):
                            word += next_char
                        i += 1
                    
    with open('%s/train.tsv' % app.config['CLASSIFIER_PATH'], 'w') as train_file:
        train_file.write(training_data)

    train_cmd = 'java -cp %s/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop %s/train.prop -trainFile %s/train.tsv -serializeTo %s/disease-ner-model.ser.gz' % (app.config["LIB_PATH"], app.config["LIB_PATH"], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'])
    system(train_cmd)
    return "true"

@app.route('/test', methods = ['POST'])
def test():
    test_data = request.form['data']
    
    with open('%s/test.txt' % app.config['CLASSIFIER_PATH'], 'w') as test_file:
        test_file.write(test_data)

    tok_command = "java -cp %s/stanford-ner.jar edu.stanford.nlp.process.PTBTokenizer %s/test.txt > %s/test.tok" % (app.config["LIB_PATH"], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'])
    system(tok_command)

    test_command = "java -cp %s/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier %s/disease-ner-model.ser.gz -testFile %s/test.tok > %s/results.txt" % (app.config["LIB_PATH"], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'])
    system(test_command)

    with open('%s/results.txt' % app.config['CLASSIFIER_PATH']) as results_file:
        results = ''
        for line in results_file.read().split('\n'):
            if line:
                (word, _, category) = line.split('\t')
                results += '<p class="%s">%s %s</p>' % (category.lower(), word, category)

        return results

def _escaped_match(text, start, word):
    if text[start:start+len(word)] == word:
        return True
    elif word == '-RRB-' and (text[start] == '>' or text[start] == ')' or text[start] == ']' or text[start:start+4] == '&lt;'):
        return True
    elif word == '-LRB-' and (text[start] == '<' or text[start] == '(' or text[start] == '[' or text[start:start+4] == '&rt;'):
        return True
    elif (word == '``' or word == '\'\'') and text[start] == '"':
        return True
    elif '\\' in word:
        no_escape_word = word.replace('\\', '')
        return no_escape_word == text[start:start+len(no_escape_word)]

@app.route('/annotate/stanford', methods = ['POST'])
def annotate_stanford():
    test_data = request.data
    
    with open('%s/test.txt' % app.config['CLASSIFIER_PATH'], 'w') as test_file:
        test_file.write(test_data)

    tok_command = "java -cp %s/stanford-ner.jar edu.stanford.nlp.process.PTBTokenizer -options americanize=false %s/test.txt > %s/test.tok" % (app.config["LIB_PATH"], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'])
    system(tok_command)

    test_command = "java -cp %s/stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier %s/disease-ner-model.ser.gz -testFile %s/test.tok > %s/results.txt" % (app.config["LIB_PATH"], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'], app.config['CLASSIFIER_PATH'])
    system(test_command)

    with open('%s/results.txt' % app.config['CLASSIFIER_PATH']) as results_file:
        annotations = {}

        lines = results_file.read().split('\n')

        line_index = 0

        for start_offset in range(0, len(test_data)):
            if lines[line_index]:
                (word, _, category) = lines[line_index].split('\t')
                end_offset = start_offset + len(word)
                if _escaped_match(test_data, start_offset,  word):
                    if category.lower() != 'other':
                        key = '%s_%i' % (word, start_offset)
                        annotations[key] = {}
                        annotations[key]['offsets'] = [[start_offset, end_offset]]
                        annotations[key]['type'] = category
                        annotations[key]['texts'] = [word]
                    line_index += 1


        return json.dumps(annotations)
