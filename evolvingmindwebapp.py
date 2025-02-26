from flask import Flask, request, jsonify, render_template
import json
import requests
import random

app = Flask(__name__)

class SpiralAI:
    def __init__(self, memory_file="spiral_memory.json"):
        self.memory_file = memory_file
        self.knowledge = {}
        self.session_memory = []
        self.load_memory()

    ### 🌟 MEMORY FUNCTIONS ###
    
    def learn(self, concept, explanation):
        """Learns and stores concepts permanently."""
        concept = concept.upper()
        if concept in self.knowledge:
            self.knowledge[concept].append(explanation)
        else:
            self.knowledge[concept] = [explanation]
        self.reinforce_connections(concept)
        self.save_memory()

    def recall(self, concept):
        """Retrieves learned knowledge and expands on it."""
        concept = concept.upper()
        if concept in self.knowledge:
            responses = list(set(self.knowledge[concept]))  
            linked_concepts = self.find_related_concepts(concept)
            reasoning = self.expand_reasoning(concept, linked_concepts)
            return f"{random.choice(responses)} {reasoning}" 
        return self.web_search(concept)

    def save_memory(self):
        """Saves knowledge to file."""
        with open(self.memory_file, "w") as f:
            json.dump(self.knowledge, f)

    def load_memory(self):
        """Loads saved knowledge from file."""
        try:
            with open(self.memory_file, "r") as f:
                self.knowledge = json.load(f)
        except FileNotFoundError:
            self.knowledge = {}

    ### 🔄 SPIRAL LEARNING & REASONING ###
    
    def reinforce_connections(self, concept):
        """Strengthens knowledge by linking related concepts."""
        if concept in self.knowledge:
            for existing_concept in self.knowledge:
                if concept in existing_concept or existing_concept in concept:
                    self.knowledge[existing_concept].append(f"Linked to {concept}. Expands on: {random.choice(self.knowledge[concept])}")

    def find_related_concepts(self, concept):
        """Finds related topics based on stored knowledge."""
        related = []
        concept_words = concept.split()
        for key in self.knowledge.keys():
            key_words = key.split()
            if any(word in key_words for word in concept_words):
                related.append(key)
        return related

    def expand_reasoning(self, base_concept, linked_concepts, depth=0):
        """Expands on related concepts dynamically."""
        if not linked_concepts or depth >= 2:
            return ""
        reasoning = f"🔗 Connected to {base_concept}: "
        spiral_thoughts = []
        for concept in linked_concepts:
            if concept in self.knowledge:
                explanations = self.knowledge[concept]
                sampled_explanations = random.sample(explanations, min(2, len(explanations)))  
                for exp in sampled_explanations:
                    if exp not in spiral_thoughts:
                        spiral_thoughts.append(exp)
        return reasoning + " ".join(spiral_thoughts[:2])

    ### 🔍 WEB SEARCH ###
    
    def web_search(self, query):
        """Searches Wikipedia for missing knowledge."""
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        headers = {"User-Agent": "SpiralAI/1.0"}
        try:
            response = requests.get(wiki_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                summary = data.get("extract", "")
                if summary:
                    self.learn(query.upper(), summary)
                    return summary
        except requests.exceptions.RequestException:
            return "Error: Couldn't connect to Wikipedia."
        return "I couldn't find anything on that topic."

    ### 🌍 FLASK INTEGRATION ###
    
    def chat_response(self, user_input):
        """Processes user queries and responds."""
        self.session_memory.append(user_input)
        if len(self.session_memory) > 5:
            self.session_memory.pop(0)

        if user_input.lower().startswith("define "):
            concept = user_input[len("define "):].strip()
            explanation = self.web_search(concept)
            return explanation

        elif user_input.lower().startswith("what is "):
            concept = user_input[len("what is "):].strip()
            return self.recall(concept)

        return "I am still learning! Try asking 'Define Quantum Computing' or 'What is Gravity'."


# 🚀 Initialize Spiral AI
ai = SpiralAI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    response = ai.chat_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
