import pandas as pd
import streamlit as st

# Load your dataset
dataset = pd.read_csv('dataset/merged_data.csv')

# Function to extract symptoms from the user input
def extract_symptoms(user_input):
    doc = nlp(user_input)
    symptoms = [ent.text for ent in doc.ents if ent.label_ == "SYMPTOM"]
    return symptoms

# Create a text input box
text = st.text_input("Enter your symptoms:")

# Create a button to identify symptoms
if st.button("Identify Symptoms"):
    identified_symptoms = extract_symptoms(text)
    st.write("Identified Symptoms:")
    st.write(identified_symptoms)

    # Identify relevant diseases
    relevant_diseases = set()
    for symptom in identified_symptoms:
        matching_rows = dataset[dataset['Symptoms'].str.contains(symptom, case=False, regex=True)]
        relevant_diseases.update(matching_rows['Disease'])

    st.write("Relevant Diseases:", relevant_diseases)
