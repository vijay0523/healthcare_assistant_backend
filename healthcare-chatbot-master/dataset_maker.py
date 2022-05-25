import json
import pandas as pd
import csv
import numpy as np
from collections import defaultdict

disease_symptom_dataset_url = "http://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html"

# Find table.
table = pd.read_html(disease_symptom_dataset_url)[0]

# Save CSV file
table.to_csv("disease_symptom_dataset_unprocessed.csv", index=False)

# Data Preprocessing
# Read CSV File
disease_symptom_dataset_unprocessed = pd.read_csv('disease_symptom_dataset_unprocessed.csv')
# Drop the first row
disease_symptom_dataset_unprocessed = disease_symptom_dataset_unprocessed.drop(0, axis=0)
# Reset Index
disease_symptom_dataset_unprocessed = disease_symptom_dataset_unprocessed.reset_index(drop=True)
# Rename columns
disease_symptom_dataset_unprocessed.columns=['disease', 'occurrences', 'symptoms']
# Handle NaN values
disease_symptom_dataset_unprocessed = disease_symptom_dataset_unprocessed.fillna(method='ffill')

save_json = {}
save_json['intents'] = []

# Function to convert   
def listToString(s):  
    
    # initialize an empty string 
    str1 = " " 
    
    # return string   
    return (str1.join(s)) 
        
# Process disease and symptoms columns
def remove_umls_code(data):
    data_ = []
    items = data.replace('^','_').split('_')
    i = 1
    for item in items:
        if (i % 2 == 0):
            data_.append(item)
        i += 1
    return data_

diseases = []
symptoms = []
occurrences = 0
disease_symptoms = defaultdict(list)
disease_symptoms_occurrences = {}
disease_symptom_df = pd.DataFrame([], columns=["diseases", "symptoms"])
for index, row in disease_symptom_dataset_unprocessed.iterrows():

    diseases = remove_umls_code(row['disease']) if (row['disease'] !="\xc2\xa0") and (row['disease'] != "") else []
    occurrences = row['occurrences'] if (row['occurrences'] !="\xc2\xa0") and (row['occurrences'] != "") else []
    symptoms = remove_umls_code(row['symptoms']) if (row['symptoms'] !="\xc2\xa0") and (row['symptoms'] != "") else []
    disease_symptom_df = disease_symptom_df.append(
        {
            "diseases": listToString(remove_umls_code(row['disease']) if (row['disease'] !="\xc2\xa0") and (row['disease'] != "") else []), 
            "symptoms":listToString(remove_umls_code(row['symptoms']) if (row['symptoms'] !="\xc2\xa0") and (row['symptoms'] != "") else [])
        }, ignore_index=True)
    
    for d in diseases:
        save_json['intents'].append([d])
        for s in symptoms:
            disease_symptoms[d].append(s)
            save_json['intents'][-1].append(s)
        disease_symptoms_occurrences[d] = occurrences
    # save_json['intents'].append([diseases[0]])
    # save_json['intents'][-1].append(symptoms)

for ds in disease_symptoms.items():
    print("'" + ds[0] + "',")
#     save_json['intents'].append([ds[0], ds[1]])
# print(save_json)
# with open('symptom_intents.json', 'w') as outfile:
#     json.dump(save_json, outfile, indent=2)
# json.dumps(save_json, indent=2)
# Save the cleaned dataset to a CSV file
# disease_symptom_dataset_unprocessed.to_csv("disease_symptom_dataset_processed.csv")
# Save disease-symptoms list to a CSV file
disease_symptoms_data = pd.DataFrame.from_dict(disease_symptoms.items())
# disease_symptoms_data.to_csv('disease_symptoms.csv')
# print(disease_symptoms_data[0])
# Save disease-symptoms-occurrences list to CSV file
# disease_symptoms_occurrences_data = pd.DataFrame.from_dict(disease_symptoms_occurrences.items())
# disease_symptoms_occurrences_data.to_csv('disease_occurrences.csv')