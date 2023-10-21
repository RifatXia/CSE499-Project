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

if st.button("Redirect"):
    st.markdown('<meta http-equiv="refresh" content="0; URL=http://127.0.0.1:8000/hospital/get_doctor/uro/">', unsafe_allow_html=True)


# while user_input:
#     # Process the text with spaCy
#     doc = nlp(user_input)

#     # Extract key points
#     key_points = [token.text for token in doc if token.pos_ == "NOUN" or token.pos_ == "ADJ"]

#     # Display the key points
#     # st.write("Extracted Key Points:")
#     # st.write(key_points)

#     # Check if each key point is present in the dataset
#     matching_diseases = set()

#     # Iterate through symptom columns
#     symptom_columns = [f'Symptom_{i}' for i in range(1, 29)]
#     for col in symptom_columns:
#         matching_rows = dataset[dataset[col].fillna('').str.contains('|'.join(key_points), case=False, regex=True)]
#         if not matching_rows.empty:
#             matching_diseases.update(matching_rows['Disease'])  
