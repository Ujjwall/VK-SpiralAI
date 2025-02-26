import json
import requests
import re

class SpiralAI:
    def __init__(self, memory_file="memory.json"):
        self.memory_file = memory_file
        self.knowledge = {}
        self.load_memory()

    def save_memory(self):
        """Saves learned knowledge to a file."""
        with open(self.memory_file, "w") as f:
            json.dump(self.knowledge, f, indent=4)

    def load_memory(self):
        """Loads stored knowledge."""
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
        self.save_memory()
        print(f"✅ Learned: {word} - {meaning}")

    def recall(self, word):
        """Retrieves stored knowledge or asks the user."""
        word = word.upper()
        if word in self.knowledge:
            return self.knowledge[word]
        else:
            return None  # No need to immediately search online

    def web_search(self, query):
        """Search Wikipedia for a topic."""
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "No information available.")

        return "I couldn't find anything on that topic."

    def compute_math(self, expression):
        """Evaluates math expressions while preventing code injection."""
        try:
            # Allow only numbers and math symbols
            if not re.match(r"^[0-9+\-*/().\s]+$", expression):
                return "I couldn't compute that expression."
            result = eval(expression)
            return f"The answer is: {result}"
        except:
            return "I couldn't compute that expression."

    def chat(self):
        """Interactive chat mode."""
        print("🤖 Spiral AI: Hello! Ask me anything or teach me something new. (Type 'exit' to quit)")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Spiral AI: Goodbye!")
                break

            # Check if input is a math problem
            if re.match(r"^\s*\d+\s*[\+\-\*/]\s*\d+\s*$", user_input):
                response = self.compute_math(user_input)
                print(f"Spiral AI: {response}")
                continue

            # Handling definitions
            if user_input.lower().startswith("define "):
                word = user_input[7:].strip()
                if word:
                    meaning = self.web_search(word)
                    if meaning and meaning != "I couldn't find anything on that topic.":
                        self.learn(word, meaning)
                    print(f"Spiral AI: {meaning}")
                else:
                    print("Spiral AI: Please specify what to define.")

            # Handling recall
            elif user_input.lower().startswith("what is "):
                word = user_input[8:].strip()
                stored_info = self.recall(word)

                if stored_info:
                    print(f"Spiral AI: {stored_info}")
                else:
                    print(f"🔍 Searching online for: {word}")
                    definition = self.web_search(word)

                    if definition and definition != "I couldn't find anything on that topic.":
                        self.learn(word, definition)
                        print(f"Spiral AI: {definition}")
                    else:
                        user_definition = input(f"❓ I don't know about {word}. Can you define it? ")
                        if user_definition:
                            self.learn(word, user_definition)
                            print(f"Spiral AI: Thanks! I have learned that {word} means: {user_definition}")
                        else:
                            print("Spiral AI: I still don't know what that is.")

            else:
                print("Spiral AI: I am still learning! Try 'Define Gravity' or 'What is Evolution'.")

# 🚀 Run AI in Terminal
if __name__ == "__main__":
    ai = SpiralAI()
    ai.chat()
