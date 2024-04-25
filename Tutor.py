from mlx_lm import load, generate

class Tutor:
    def __init__(self):
        self.model, self.tokenizer = load("mlx-community/dolphin-2.9-llama3-8b-8bit")

    def format_as_bulleted_list(self, variable):
        # Check if the variable is a string
        if isinstance(variable, str):
            return variable

        # Check if the variable is a list and all elements are strings
        elif isinstance(variable, list) and all(isinstance(item, str) for item in variable):
            # Create a bullet-pointed string
            return '\n'.join(f'- {item}' for item in variable)
        
        # If variable is neither a string nor a list of strings, return an error message
        else:
            return "Given answer is neither a string nor list."
        
    def write_explanation(self, question, incorrect_answer, correct_answer):
        prompt = "You are an online tutor who explains why answers given to multiple-choice questions are incorrect in an engaging and factual manner. It is your job to read a question that was incorrectly answered, the incorrect answer that was given, the correct answer, and to write an explanation in a constructive and patient tone as to why the given answer was wrong, and why the correct answer is what it is. These multiple-choice questions can have either one or multiple correct answers."
        prompt += "Your response should be a few sentences, up to a paragraph. Feel free to insert interesting context for why one answer is right and the other is wrong, so that the user who supplied the answer might have context to better remember the answer next time they see it.\n"
        prompt += "The explanation should be written as though an empathetic textbook were giving context to a supplied answer key. Factual, interesting, but not too personal. Your explanations should be written directly addressing the user who answered the question; don't talk about \"the student\" or anything like that, just write the note directly to the user who selected the answer(s). When writing the feedback just get directly into the notes, don't bring up any meta-context. Feel free to insert line  breaks where appropriate.\n"
        prompt += "For example, if the question was \"Which elements are gases at room temperature?\" and the student selected \n- Oxygen\n- Carbon\n- Nitrogen\nwhile the correct answer was to have selected\n- Oxygen\n- Nitrogen\n- Helium\nthen at the end of your final output should be something along the lines of:\nThe given answer is almost correct, but got one answer wrong. While Oxygen and Nitrogen are gases at room temperature, Carbon is a solid, while Helium is still a gas at room temperature. This is why baloons float!\n"
        prompt += f"\n\nHere is the question that the student got wrong:\n{question}\n\nHere is the answer that the student gave:\n{self.format_as_bulleted_list(incorrect_answer)}\n\nHere is the expected answer:\n{self.format_as_bulleted_list(correct_answer)}"


        response = generate(self.model, self.tokenizer, prompt=prompt, verbose=True, max_tokens=1000)
        return response