import streamlit as st
import pickle
import spacy
import pandas as pd

# Setting the page configuration
st.set_page_config(page_title="Disease Detection", page_icon="", layout="wide")
st.title("Disease Detection")

# Importing the model and the pickle dataset
symptoms = pickle.load(open("symptoms.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
symptoms_list = symptoms.to_dict(orient='records')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load the dataset
dataset = pd.read_csv('dataset/merged_data_2.csv')

# Initialize user input
user_input = st.text_input("Describe your symptoms:")

# Process the text with spaCy
doc = nlp(user_input)

# Extract key points
key_points = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "ADJ"]

# Check if each key point is present in the dataset
matching_diseases = set()

# Iterate through symptom columns
symptom_columns = [f'Symptom {i}' for i in range(1, 29)]
for col in symptom_columns:
    matching_rows = dataset[dataset[col].fillna('').str.contains('|'.join(key_points), case=False, regex=True)]
    if not matching_rows.empty:
        matching_diseases.update(matching_rows['Disease'])

symptom_frequency = {}
for disease in matching_diseases:
        symptoms_in_disease = [dataset.loc[dataset['Disease'] == disease, f'Symptom {i}'].values[0] for i in range(1, 29)]
        symptoms_in_disease = [symptom for symptom in symptoms_in_disease if pd.notna(symptom)] 

        # Remove symptoms mentioned by the user
        symptoms_in_disease = [symptom for symptom in symptoms_in_disease if symptom not in key_points]

         # Update symptom frequency
        for symptom in symptoms_in_disease:
            if symptom in symptom_frequency:
                symptom_frequency[symptom] += 1
            else:
                symptom_frequency[symptom] = 1

symptom_frequency = dict(sorted(symptom_frequency.items(), key=lambda item: item[1], reverse=True))

# Print the symptom frequencies
st.write("Symptom Frequencies:")
for symptom, frequency in symptom_frequency.items():
    st.write(f"{symptom}: {frequency}")

categories = {
    'uro': ['Urinary tract infection', 'Kidney Disease', 'Bladder Disorder'],
    'psy': ['Bipolar Disorder', 'Schizophrenia', 'Delusion', 'Manic Disorder', 'Depressive Disorder', 'Paranoia'],
    'cancer': ['Melanoma', 'Prostate Cancer', 'Carcinoma of Lung', 'Breast Infiltrating Ductal Carcinoma'],
    'gas': ['Gastroenteritis', 'Peptic ulcer disease', 'Duodenal ulcer', 'Aphthous Stomatitis', 'Gastritis', 'Gastrointestinal Hemorrhage'],
    'skin': ['Psoriasis', 'Acne', 'Fungal infection'],
    'med': ['Hypertension', 'Diabetes', 'Hypoglycemia', 'Chronic Kidney Failure', 'Obesity', 'Hyperlipidemia'],
    'gyn': ['Cervical spondylosis', 'Polycystic Ovary Syndrome', 'Endometriosis', 'Cervical Dysplasia', 'Leiomyoma', 'Menstruation Disorders'],
    'car': ['Myocardial Infarction', 'Atherosclerosis', 'Ischemia', 'Coronary Heart Disease', 'Angina Pectoris'],
    'art': ['Arthritis', 'Joint Pain', 'Spondylolisthesis', 'Arthropathy', 'Osteoarthritis', 'Fibromyalgia'],
    'ear': ['Ear Infection', 'Tinnitus', 'Hearing Problem', 'Otitis Media', 'Meniere Disease', 'Acoustic Neuroma'],
    'misc': ['Bacteremia', 'Parkinson Disease', 'Hyperglycemia', 'Failure Heart', 'Obesity Morbid', 'Confusion', 'Sickle Cell Anemia', 'Tonic-Clonic Seizures', 'Herniahiatal', 'Osteoarthristis', 'Primary Carcinoma Of The Liver Cells', 'Migraine Disorders', 'Alcoholic hepatitis', 'Hypercholesterolemia', 'Obesity', 'Upper Respiratory Infection', 'Neutropenia', 'Ileus', 'Cholecystitis', 'Lymphatic Diseases', 'Anxiety State', 'Pericardial Effusion Body Substance', 'Personality Disorder', 'AIDS', 'Failure Kidney', 'Malaria', 'Hyperlipidemia', 'Hypertension ', 'Schizophrenia', 'Influenza', 'Dementia', 'Cervical spondylosis', 'HIV Infections', 'Pancreatitis', 'Depressive Disorder', 'Hypoglycemia', 'Hemorrhoids', 'Hepatitis E', 'Insufficiency Renal', 'Osteoporosis', 'Gastroenteritis', 'Endocarditis', 'Transient Ischemic Attack', 'Pneumocystiscariniipneumonia', 'Cirrhosis', 'Ischemia', 'Deglutition Disorder', 'Lymphoma', 'Diverticulitis', 'Common Cold', 'Delusion', 'Drug Reaction', 'Stenosis Aortic Valve', 'Primary Malignant Neoplasm', 'Melanoma', 'hepatitis A', 'Hemiparesis', 'Jaundice', 'Gastroesophageal Reflux Disease', 'Tuberculosis', 'Manic Disorder', 'Myocardial Infarction', 'Colitis', 'Bronchial Asthma', 'Failure Heart Congestive', 'Accidentcerebrovascular', 'Pancytopenia', 'Pyelonephritis', 'Carcinoma', 'Mitral Valve Insufficiency', 'Dimorphic hemmorhoids(piles)', 'Hyperthyroidism', 'Oralcandidiasis', 'Pneumothorax', 'Asthma', 'Hyperbilirubinemia', 'Benign Prostatic Hypertrophy', 'Dengue', 'Thrombocytopaenia', "Alzheimer'S Disease", '(vertigo) Paroymsal  Positional Vertigo', 'Arthritis', 'Neuropathy', 'Hypertension Pulmonary', 'Peripheral Vascular Disease', 'Chicken pox', 'Carcinoma Of Lung', 'Cardiomyopathy', 'Emphysema Pulmonary', 'Hypertensive Disease', 'Hypothyroidism', 'Diabetes', 'Varicose veins', 'Gastritis', 'Peptic ulcer diseae', 'Psychotic Disorder', 'Typhoid', 'Chronic Kidney Failure', 'Tricuspid Valve Insufficiency', 'Cellulitis', 'Biliary Calculus', 'Kidney Failure Acute', 'Hernia', 'Neoplasm', 'Encephalopathy', 'Dehydration', 'Infection', 'Diabetes ', 'Adenocarcinoma', 'Paralysis (brain hemorrhage)', 'Hepatitis C', 'Embolism Pulmonary', 'Ketoacidosis Diabetic', 'Degenerativepolyarthritis', 'Malignantneoplasms', 'Hepatitis B', 'Infection Urinary Tract', 'Bronchitis', 'Fibroid Tumor', 'GERD', 'Diverticulosis', 'Neoplasm Metastasis', 'Delirium', 'Pneumonia Aspiration', 'Glaucoma', 'Gout', 'Osteomyelitis', 'Hepatitis D', 'Thrombus', 'Incontinence', 'Chronic Alcoholic Intoxication', 'Kidney Disease', 'Overload Fluid', 'Hepatitis', 'Edema Pulmonary', 'Allergy', 'Chronic cholestasis', 'Pneumonia', 'Paroxysmaldyspnea', 'Dependence', 'Tachycardia Sinus', 'Affect Labile', 'Decubitus Ulcer', 'Exanthema', 'Migraine', 'Carcinoma Colon', 'Spasm Bronchial', 'Aphasia', 'Deep Vein Thrombosis', 'Anemia', 'Respiratory Failure', 'Carcinoma Prostate', 'Chronic Obstructive Airway Disease', 'Suicide Attempt', 'Epilepsy', 'Impetigo', 'Coronary Heart Disease', 'Sepsis (Invertebrate)', 'Carcinoma Breast', 'Ulcer Peptic', 'Adhesion', 'Paranoia', 'Heart attack'],
}

disease_name = 'Bipolar Disorder'
keyword = ""
for ind in categories:
    for name in categories[ind]:
        if name == disease_name:
            keyword = ind 

if st.button("Get appointment"):
    url = f'http://127.0.0.1:8000/hospital/get_doctor/{keyword}/'
    st.markdown(f'<meta http-equiv="refresh" content="0; URL={url}">', unsafe_allow_html=True)