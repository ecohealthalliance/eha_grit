from flask import Flask, request
import json, csv, re
application = Flask(__name__)

diseases = []
symptoms = []

@application.route("/", methods=['GET', 'POST'])
def annotate():
    if len(diseases) < 1:
        load_data()

    text = request.data

    annotations = {}

    for start_offset in range(0, len(text)):
        if start_offset == 0 or text[start_offset - 1] == ' ':
            for end_offset in range(start_offset, len(text)):
                if text[end_offset] == ' ':
                    word = text[start_offset:end_offset]
                    if word.lower() in diseases: 
                        key = '%s_%i' % (word, start_offset)
                        annotations[key] = {}
                        annotations[key]['offsets'] = [[start_offset, end_offset]]
                        annotations[key]['type'] = 'disease'
                        annotations[key]['texts'] = [word]
                    elif word.lower() in symptoms:
                        key = '%s_%i' % (word, start_offset)
                        annotations[key] = {}
                        annotations[key]['offsets'] = [[start_offset, end_offset]]
                        annotations[key]['type'] = 'symptom'
                        annotations[key]['texts'] = [word]
                    break

    return json.dumps(annotations)

def load_data():
    with open('Matrix_symp_dis.csv', 'rU') as f:
        reader = csv.reader(f)
        
        global diseases, symptoms
        diseases = [' '.join(disease.split('_')).lower() for disease in reader.next()[1:]]

        # http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
        first_cap_re = re.compile('(.)([A-Z][a-z]+)')
        all_cap_re = re.compile('([a-z0-9])([A-Z])')
        def convert(name):
            s1 = first_cap_re.sub(r'\1 \2', name)
            return all_cap_re.sub(r'\1 \2', s1).lower()


        symptoms = [convert(row[0]) for row in reader]


if __name__ == "__main__":
    application.run(port=5001)
