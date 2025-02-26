from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__, template_folder="C:/Users/ujjwa/Downloads/templates_")  # Update this path

class SpiralAI:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.knowledge = {}
        self.load_memory()

    def save_memory(self):
        """Saves learned knowledge to memory.json."""
        try:
            with open(self.memory_file, "w") as f:
                json.dump(self.knowledge, f, indent=4)
        except Exception as e:
            print(f"Error saving memory: {e}")

    def load_memory(self):
        """Loads stored knowledge from memory.json."""
        try:
            with open(self.memory_file, "r") as f:
                self.knowledge = json.load(f)
            print("🧠 Memory Loaded Successfully!")
        except FileNotFoundError:
            print("🔄 No memory found, starting fresh.")
            self.knowledge = {}

    def learn(self, word, meaning):
        """Stores new knowledge and saves it."""
        word = word.upper()
        self.knowledge[word] = meaning
        self.save_memory()  # Save updates immediately
        return f"✅ Learned: {word} - {meaning}"

    def recall(self, word):
        """Retrieves stored knowledge."""
        word = word.upper()
        return self.knowledge.get(word, None)

    def compute_math(self, expression):
        """Evaluates basic arithmetic expressions."""
        try:
            result = eval(expression)
            return f"The answer is: {result}"
        except Exception:
            return "I couldn't compute that expression."

    def process_query(self, user_input):
        """Processes user input and returns an AI response."""
        user_input = user_input.strip()

        # Handle mathematical computations
        if re.match(r"^\s*\d+\s*[\+\-\*/]\s*\d+\s*$", user_input):
            return self.compute_math(user_input)

        # Handle definitions
        if user_input.lower().startswith("define "):
            word = user_input[7:].strip()
            return f"Okay! What does '{word}' mean?"

        # Handle learning (user provides definition)
        if " - " in user_input:
            parts = user_input.split(" - ")
            if len(parts) == 2:
                return self.learn(parts[0].strip(), parts[1].strip())

        # Handle recall of known concepts
        elif user_input.lower().startswith("what is "):
            word = user_input[8:].strip()
            stored_info = self.recall(word)

            if stored_info:
                return stored_info
            else:
                return f"🔍 I don't know about {word} yet. Can you define it?"

        return "I am still learning! Try asking 'Define Gravity' or 'What is Evolution'."


# Initialize Spiral AI Model
spiral_ai = SpiralAI()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a valid message."})

    response = spiral_ai.process_query(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
