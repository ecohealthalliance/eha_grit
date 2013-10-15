import csv, operator

diseases_by_symptom = None

def _load_symptom_map():
	with open('classifier/matrix/Master_clean_gideon_comparison.csv') as f:
		reader = csv.reader(f)
		reader.next()
		return dict([(row[0], row[1]) for row in reader])

def _load_matrix_data():
	disease_map = {
	    'Bacterial Meningitis' : 'Meningitis-bacterial',
	    'Dengue' : 'Dengue',
	    'JE' : 'Japanese Encephalitis',
	    'Measles' : 'Measles',
	    'Malaria' : 'Malaria',
	    'Meningitis-aseptic' : 'Meningitis -aseptic (viral)',
	    'Nipah Virus' : 'Nipah and Nipah-like Virus Disease',
	    'Typhoid/Enteric Fever' : 'Typhoid and Enteric Fever',
	    'Chandipura' : 'Chandipura and Vesicular stomatitis viruses',
	    'Chikungunya' : 'Chikungunya',
	}

	global diseases_by_symptom
	with open('classifier/matrix/Matrix_symp_dis_v4.csv') as f:
		reader = csv.DictReader(f, delimiter='\t')
		diseases_by_symptom = {}
		for row in reader:
			diseases_by_symptom[row.get('Symptom')] = [disease for disease, present in row.iteritems() if present is '1' and disease in disease_map.values()]
		return diseases_by_symptom

def _diagnose(symptoms):
	if not diseases_by_symptom:
		_load_matrix_data()
	possible_diseases = {}
	for symptom in symptoms:
		for disease in diseases_by_symptom.get(symptom) or []:
			if not possible_diseases.get(disease):
				possible_diseases[disease] = []
			possible_diseases[disease].append(symptom)
	return possible_diseases

def classify(train, test):
	symptom_map = _load_symptom_map()

	diagnoses = []
	others = []
	for item in test:
		present_symptoms = []
		for symptom, value in item.get('attr').iteritems():
			gideon_symptom = symptom_map.get(symptom)
			if gideon_symptom and value not in [0, '0', 'n', '']:
				present_symptoms.append(gideon_symptom)
		possible_diseases = _diagnose(present_symptoms)
		if len(possible_diseases):
			diagnosis = max(possible_diseases.iterkeys(), key=(lambda (key): len(possible_diseases[key])))
			diagnoses.append(diagnosis)
			others.append(possible_diseases)
		else:
			diagnoses.append('Unknown')
			others.append({})
	return (diagnoses, others)



