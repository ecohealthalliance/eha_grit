import json, re, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pylab import arange

def plot_symptoms(disease):
    report_symptoms = []

    disease_regex = re.compile(disease)

    with open('promed_symptoms.json') as f:
        nodes = json.loads(f.read())["nodes"]

        for node in nodes:
            match = disease_regex.search(node.get('title'))
            if match:
                symptoms = node.get('symptoms')
                date = node.get('promed_id').split('.')[0]
                report_symptoms.append({'symptoms': symptoms, 'date': date})

    symptoms_with_date = {}
    dates = set([])

    for report in report_symptoms:
        date = report.get('date')
        dates.add(date)
        for symptom in report.get('symptoms'):
            if not symptoms_with_date.get(symptom):
                symptoms_with_date[symptom] = set([])
            symptoms_with_date[symptom].add(date)

    symptom_list = [symptom for symptom in symptoms_with_date.iterkeys()]
    sorted_symptoms = sorted(symptom_list, key=lambda symptom: -int(min(symptoms_with_date[symptom])))

    first_dates = [min(symptoms_with_date[symptom]) for symptom in sorted_symptoms]
    first_dates = [mdates.date2num(datetime.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))) for d in first_dates]
    last_dates = [max(symptoms_with_date[symptom]) for symptom in sorted_symptoms]
    last_dates = [mdates.date2num(datetime.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))) for d in last_dates]

    lengths = [last - first for (last, first) in zip(last_dates, first_dates)]
    y_pos = arange(len(sorted_symptoms)) + .5

    plt.clf()
    fig, ax = plt.subplots(figsize=(15,15))
    ax.barh(y_pos, lengths, left=first_dates, align='center')
    plt.yticks(y_pos, sorted_symptoms)
    ax.xaxis_date()

    plt.savefig('symptoms - %s.png' % disease)

if __name__ == '__main__':
    plot_symptoms('Novel coronavirus')
    plot_symptoms('H7N9')

