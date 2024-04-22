import json

# Define the JSON fie path
json_file_path = 'ExampleQuestions.json'

# Function to add seqeuntial Ids to questions
def add_ids_to_questions(questions):
    for i, question in enumerate(questions):
        question['id'] = f'{i:03d}'
        # Let's reformat the ids in a more sane way
        # Get the options, and the correct selection
        if 'correct' in question:
            options = question['options']
            correct = question['correct']
            
            updated_options = [{"text": option, "isCorrect": (option in correct)} for option in options]

            question['options'] = updated_options

            del question["correct"]


# Read the JSON file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Ensure the JSON data is a list
if isinstance(data['questions'], list):
    # Add Ids to questions
    add_ids_to_questions(data['questions'])

    # Update the JSON file with the new data
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print("Ids added and JSON file updated successsfully.")
else:
    print("JSON data is not in the expected list format.")