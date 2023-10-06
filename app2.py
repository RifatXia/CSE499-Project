import streamlit as st
import pickle
import numpy as np

# setting the page configuration
st.set_page_config(page_title="Disease Detection", page_icon="", layout="wide")
st.title("Disease Detection")

# importing the model and the pickle dataset
symptoms = pickle.load(open("symptoms.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

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
symptoms_map = {symptom: 0 for symptom in sorted(symptoms["Symptoms"].unique())}
for i, selectbox_value in enumerate(st.session_state.selectbox_data['values']):
    disease_name = st.selectbox(f"Symptom {i + 1}", sorted(symptoms["Symptoms"].unique()))
    symptoms_map[disease_name] = 1
    if st.button(f"Remove Symptom {i + 1}"):
        remove_selectbox(i)

user_input = np.array(list(symptoms_map.values()), dtype=np.int64).reshape(1, -1)


if st.button("Get Disease"):
    predicted_disease = model.predict(user_input)[0]
    st.title(predicted_disease)
