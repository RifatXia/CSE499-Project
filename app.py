import streamlit as st
import pickle
import numpy as np
import sklearn

# setting the page configuration 
st.set_page_config(page_title="Disease Detection", page_icon="", layout="wide")
st.title("Disease Detection")

# importing the model and the pickle dataset 
symptoms = pickle.load(open("symptoms.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))
symptoms_list = symptoms.to_dict(orient='records')

# Dynamic selection box 
if 'selectbox_data' not in st.session_state:
    st.session_state.selectbox_data = {'count': 0, 'values': []}

# Function to add a selectbox
def add_selectbox():
    st.session_state.selectbox_data['count'] += 1
    st.session_state.selectbox_data['values'].append(f"Selectbox {st.session_state.selectbox_data['count']}")

# Function to remove a selectbox
def remove_selectbox(selectbox_index):
    st.session_state.selectbox_data['count'] -= 1
    st.session_state.selectbox_data['values'].pop(selectbox_index)

# Create a "plus" button to add a selectbox
if st.button("Add Symptom"):
    add_selectbox()

# Create selectboxes
symptoms_map = {symptom['Symptoms']: 0 for symptom in symptoms_list}
for i, selectbox_value in enumerate(st.session_state.selectbox_data['values']):
    # keeping track of the symptoms
    unique_symptoms = sorted(symptoms["Symptoms"].unique())
    disease_name = st.selectbox(f"Symptom {i + 1}", unique_symptoms)
    symptoms_map[disease_name] = 1
    if st.button(f"Remove Symptom {i + 1}"):
        remove_selectbox(i)

user_input = [value for value in symptoms_map.values()]

if st.button("Get Disease"):
    predicted_disease = model.predict([user_input])
    st.title(predicted_disease)