from glob import glob
import re, json, csv

symptoms = []
diseases = []
matched_symptoms = set([])

def _find_symptoms(text):
    if len(diseases) < 1:
        _load_matrix_data()

    text_symptoms = set()

    for start_offset in range(0, len(text)):
        if start_offset == 0 or text[start_offset - 1] == ' ':
            for end_offset in range(start_offset, len(text)):
                if text[end_offset] == ' ' or text[end_offset] == ',' or text[end_offset] == '.' or end_offset == len(text) - 1:
                    word = text[start_offset:end_offset]
                    if word.lower() in symptoms:
                        text_symptoms.add(word.lower())
                    break

    return [symptom for symptom in text_symptoms]


def _load_matrix_data():
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
    

if __name__ == '__main__':

    REPORT_PATH = '../brat-v1.3_Crunchy_Frog/data/promed/'
    files = glob('%s/*.txt' % REPORT_PATH)

    report_id_regex = re.compile('\d{8}\.\d+')
    label_regex = re.compile('>.*?Archive Number')
    source_regex = re.compile('Source:.*?  ')

    promed_ids = []
    nodes = []
    edges = []
    links = []
    for file in files:
        with open(file) as f:
            report = f.read()
            report_ids = report_id_regex.findall(report)

            if report_ids:
                match = label_regex.search(report)
                if match:
                    label = match.group(0)[1:-14].strip()
                else:
                    label = ''

                disease = label.split('update')[0].split(' - ')[0].strip()

                temp = label.split(' - ')
                if len(temp) > 1:
                    location = temp[1].split('(')[0].strip()
                else:
                    location = ''

                source_match = source_regex.search(report)
                if source_match:
                    source = source_match.group(0)[7:-1].strip()
                else:
                    source = ''

                matched_symptoms = _find_symptoms(report)

                promed_ids.append(report_ids[0])
                nodes.append({'promed_id': report_ids[0], 'title': label, 'disease': disease, 'location': location, 'source_organization': source, 'symptoms': matched_symptoms})
                for report_id in report_ids[1:]:
                    edges.append((report_ids[0], report_id))

    for edge in edges:
        if edge[0] in promed_ids and edge[1] in promed_ids:
            links.append({'source': edge[0], 'target': edge[1]})

    result = {'nodes': nodes, 'links': links}

    print json.dumps(result)



