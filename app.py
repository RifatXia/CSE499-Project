import streamlit as st
import pickle
import spacy
import pandas as pd

# setting the page configuration 
st.set_page_config(page_title="Disease Detection", page_icon="", layout="wide")
st.title("Disease Detection")

# importing the model and the pickle dataset 
symptoms = pickle.load(open("symptoms.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
symptoms_list = symptoms.to_dict(orient='records')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load the dataset
dataset = pd.read_csv('dataset\merged_data_2.csv')

# Create a text input box
text = st.text_input("Enter your text:")

# Create a button to display the key points:
if st.button("Show Key Points"):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract key points
    key_points = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "ADJ"]

    # Display the key points
    st.write("Extracted Key Points:")
    st.write(key_points)

    # Check if each key point is present in the dataset
    matching_diseases = set()

    # Iterate through symptom columns
    for col in dataset.columns:
        if col.startswith('Symptom_'):
            # Handle NaN values by filling them with an empty string
            matching_rows = dataset[dataset[col].fillna('').str.contains('|'.join(key_points), case=False, regex=True)]
            matching_diseases.update(matching_rows['Disease'])

    # Display matching diseases
    st.write("Identified Diseases:")
    st.write(list(matching_diseases))

    # ...

    # Ask follow-up questions for each identified disease
    for disease in matching_diseases:
        st.write(f"Follow-up questions for {disease}:")

        # Assuming symptoms are stored in columns like 'Symptom_1', 'Symptom_2', ..., 'Symptom_28'
        symptoms_in_disease = [dataset.loc[dataset['Disease'] == disease, f'Symptom_{i}'].values[0] for i in range(1, 29)]

        # Remove NaN values from symptoms_in_disease
        symptoms_in_disease = [symptom for symptom in symptoms_in_disease if pd.notna(symptom)]

        # Display symptoms for the disease
        
        st.write(", ".join(symptoms_in_disease))

    
