import json

# Define the JSON fie path
json_file_path = 'ExampleQuestions.json'

# Function to add seqeuntial Ids to questions
def add_ids_to_questions(questions):
    for i, question in enumerate(questions):
        question['id'] = f'{i:03d}'

# Read the JSON file
with open(json_file_path, 'r') as file:
    questions_data = json.load(file)

# Ensure the JSON data is a list
if isinstance(questions_data, list):
    # Add Ids to questions
    add_ids_to_questions(questions_data)

    # Update the JSON file with the new data
    with open(json_file_path, 'w') as file:
        json.dump(questions_data, file, indent=2)

    print("Ids added and JSON file updated successsfully.")
else:
    print("JSON data is not in the expected list format.")