import streamlit as st
import pandas as pd

# Load your dataset
dataset_path = "dataset/preprocessed_dataset.csv"
dataset = pd.read_csv(dataset_path)

# Function to determine potential diseases based on symptoms
def determine_disease(symptoms):
    potential_diseases = set()
    for _, row in dataset.iterrows():
        if all(row[symptom] == 1 for symptom in symptoms):
            potential_diseases.add(row["Disease"])
    return potential_diseases

# Setting the page configuration
st.set_page_config(page_title="Disease Detection", page_icon="", layout="wide")
st.title("Disease Detection")

# User input for symptoms
user_input = st.text_input("Describe your symptoms (comma-separated):")

if user_input:
    # Split user input into a list of symptoms and preprocess them
    user_input = user_input.lower().replace(" ", "_")
    symptoms = user_input.split(', ')

    # Determine potential diseases
    potential_diseases = determine_disease(symptoms)

    st.write("Potential Diseases:")
    st.write(potential_diseases)

    # You can continue to ask more questions or provide information to narrow down further

# End the conversation
st.text("Type 'end' to finish the conversation.")