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

# # Dynamic selection box 
# if 'selectbox_data' not in st.session_state:
#     st.session_state.selectbox_data = {'count': 0, 'values': []}

# # Function to add a selectbox
# def add_selectbox():
#     st.session_state.selectbox_data['count'] += 1
#     st.session_state.selectbox_data['values'].append(f"Selectbox {st.session_state.selectbox_data['count']}")

# # Function to remove a selectbox
# def remove_selectbox(selectbox_index):
#     st.session_state.selectbox_data['count'] -= 1
#     st.session_state.selectbox_data['values'].pop(selectbox_index)

# # Create a "plus" button to add a selectbox
# if st.button("Add Symptom"):
#     add_selectbox()

# # Create selectboxes
# symptoms_map = {symptom['Symptoms']: 0 for symptom in symptoms_list}
# for i, selectbox_value in enumerate(st.session_state.selectbox_data['values']):
#     # keeping track of the symptoms
#     unique_symptoms = sorted(symptoms["Symptoms"].unique())
#     disease_name = st.selectbox(f"Symptom {i + 1}", unique_symptoms)
#     symptoms_map[disease_name] = 1
#     if st.button(f"Remove Symptom {i + 1}"):
#         remove_selectbox(i)

# user_input = [value for value in symptoms_map.values()]

# if st.button("Get Disease"):
#     predicted_disease = model.predict([user_input])
#     st.title(predicted_disease)

# NLP Impelementations
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
        if col.startswith('Symptom'):
            # Handle NaN values by filling them with an empty string
            matching_rows = dataset[dataset[col].fillna('').str.contains('|'.join(key_points), case=False, regex=True)]
            matching_diseases.update(matching_rows['Disease'])

    # Display matching diseases
    st.write("Identified Diseases:")
    st.write(list(matching_diseases))

    # # Ask follow-up questions for each identified disease
    # for disease in matching_diseases:
    #     st.write(f"Follow-up questions for {disease}:")

    #     # Assuming symptoms are stored in columns like 'Symptom_1', 'Symptom_2', ..., 'Symptom_28'
    #     symptoms_in_disease = [dataset.loc[dataset['Disease'] == disease, f'Symptom {i}'].values[0] for i in range(1, 29)]

    #     # Remove NaN values from symptoms_in_disease
    #     symptoms_in_disease = [symptom for symptom in symptoms_in_disease if pd.notna(symptom)]

    #     # Display symptoms for the disease
        
    #     st.write(", ".join(symptoms_in_disease))

    # Ask follow-up questions for each identified disease
    # Ask follow-up questions for each identified disease
    for disease in matching_diseases:
        st.write(f"Follow-up questions for {disease}:")

        # Find the maximum symptom index for this disease
        max_symptom_index = dataset.loc[dataset['Disease'] == disease, 'Symptom_Index'].max()

        # Assuming symptoms are stored in columns like 'Symptom_1', 'Symptom_2', ..., 'Symptom_max_symptom_index'
        symptoms_in_disease = []
        for i in range(1, max_symptom_index + 1):
            # Check if the disease is present in the filtered dataset
            if not dataset.loc[dataset['Disease'] == disease].empty:
                # Append the symptom to the list
                symptoms_in_disease.append(dataset.loc[dataset['Disease'] == disease, f'Symptom_{i}'].values[0])

        # Remove NaN values from symptoms_in_disease
        symptoms_in_disease = [symptom for symptom in symptoms_in_disease if pd.notna(symptom)]

        # Display symptoms for the disease
        st.write(f"Symptoms for {disease}:")
        st.write(", ".join(symptoms_in_disease))

        # Ask follow-up questions dynamically based on symptoms
        for symptom in symptoms_in_disease:
            user_input = st.text_input(f"Do you have {symptom.lower()}? (yes/no)")

            # Process user input and ask relevant follow-up questions
            if user_input.lower() == 'yes':
                # Ask additional questions based on your dataset
                additional_questions = dataset.loc[dataset['Disease'] == disease, 'FollowUpQuestions'].values[0].split(',')

                # Iterate through additional questions
                for additional_question in additional_questions:
                    user_response = st.text_input(f"{additional_question} (yes/no)")
                    # Process user response and ask more questions or provide a result based on your logic

            elif user_input.lower() == 'no':
                # Ask different questions or narrow down possibilities based on user's response
                other_symptom = st.text_input(f"Do you have an alternative symptom related to {symptom.lower()}?")

                if other_symptom.lower() == 'yes':
                    # Ask more questions based on your dataset
                    additional_questions = dataset.loc[dataset['Disease'] == disease, 'AlternativeQuestions'].values[0].split(',')

                    # Iterate through additional questions
                    for additional_question in additional_questions:
                        user_response = st.text_input(f"{additional_question} (yes/no)")
                        # Process user response and ask more questions or provide a result based on your logic

                elif other_symptom.lower() == 'no':
                    # Ask different questions or narrow down possibilities based on your dataset
                    st.write("Provide result or ask further questions based on your logic...")

                else:
                    st.write("Invalid input. Please enter yes or no.")

            



    