import pandas as pd

# Read the CSV file
df = pd.read_csv('dataset/data_2.csv')

# Initialize lists to store rows for the output CSV
output_data = []

current_disease = None
current_symptoms = []

# Iterate through the rows of the DataFrame
for index, row in df.iterrows():
    disease = row.iloc[0]

    if pd.notna(disease):
        # If a new disease is encountered, store the previous disease and its symptoms
        if current_disease is not None:
            # Create a new row with disease name in the first column
            output_row = [current_disease] + current_symptoms
            output_data.append(output_row)

        # Start a new disease
        current_disease = disease
        current_symptoms = []

    # Extract symptom names and add them to the current disease's symptoms
    symptom = row.iloc[1]
    if pd.notna(symptom):
        current_symptoms.append(symptom)

# Append the last disease and its symptoms
if current_disease is not None:
    output_row = [current_disease] + current_symptoms
    output_data.append(output_row)

# Create a new DataFrame for the processed data
output_df = pd.DataFrame(output_data)

# Define column names for the output DataFrame
num_symptoms = len(output_df.columns) - 1
column_names = ['Disease'] + \
    [f'Symptom_{i}' for i in range(1, num_symptoms + 1)]
output_df.columns = column_names

# Save the processed data to a CSV file
output_df.to_csv('dataset/processed_data_2.csv', index=False)
