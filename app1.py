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
dataset = pd.read_csv('dataset/merged_data.csv')

# Initialize user input
user_input = st.text_input("Describe your symptoms:")

while user_input:
    # Process the text with spaCy
    doc = nlp(user_input)

    # Extract key points
    key_points = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "ADJ"]

    # Display the key points
    # st.write("Extracted Key Points:")
    # st.write(key_points)

    # Check if each key point is present in the dataset
    matching_diseases = set()

    # Iterate through symptom columns
    symptom_columns = [f'Symptom_{i}' for i in range(1, 29)]
    for col in symptom_columns:
        matching_rows = dataset[dataset[col].fillna('').str.contains('|'.join(key_points), case=False, regex=True)]
        if not matching_rows.empty:
            matching_diseases.update(matching_rows['Disease'])

    # st.write("Matching Diseases:", list(matching_diseases))

    # Ask follow-up questions for each identified disease
    for disease in matching_diseases:
        st.write(f"Follow-up questions for {disease}:")

        # Assuming symptoms are stored in columns like 'Symptom_1', 'Symptom_2', ..., 'Symptom_29'
        symptoms_in_disease = [dataset.loc[dataset['Disease'] == disease, f'Symptom_{i}'].values[0] for i in range(1, 29)]

        # Remove NaN values from symptoms_in_disease
        symptoms_in_disease = [symptom for symptom in symptoms_in_disease if pd.notna(symptom)]

        for i in range(0, len(symptoms_in_disease)):
            symptom = symptoms_in_disease[i]
            unique_key = f"{disease}_{symptom.lower()}"
            user_input = st.text_input(f"Do you have {symptom.lower()}? (yes/no)", key=unique_key)
      
