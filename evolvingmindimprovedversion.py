import json
import requests
import random

class SpiralAI:
    def __init__(self, memory_file="spiral_memory.json"):
        self.memory_file = memory_file
        self.knowledge = {}  # Stores learned knowledge
        self.session_memory = []  # Stores recent interactions
        self.load_memory()

    ### 🌟 MEMORY FUNCTIONS ###
    
    def learn(self, concept, explanation):
        """Learns and links a concept to related knowledge."""
        concept = concept.upper()
        
        if concept in self.knowledge:
            self.knowledge[concept].append(explanation)
        else:
            self.knowledge[concept] = [explanation]

        # 🔥 Auto-Link Related Knowledge!
        related_concepts = self.find_related_concepts(concept)
        if related_concepts:
            for related in related_concepts:
                self.knowledge[related].append(f"Related to {concept}: {explanation}")
                self.knowledge[concept].append(f"Connected to {related}: {random.choice(self.knowledge[related])}")

        self.reinforce_connections(concept)
        self.save_memory()
        print(f"✅ Learned: {concept} - {explanation}")

    def recall(self, concept):
        """Retrieves a learned concept and expands its connections."""
        concept = concept.upper()

        if concept in self.knowledge:
            responses = list(set(self.knowledge[concept]))  # Remove duplicates
            linked_concepts = self.find_related_concepts(concept)
            reasoning = self.expand_reasoning(concept, linked_concepts)

            return f"{random.choice(responses)} {reasoning}"  # Pick a non-redundant response

        # 🔍 Smart Contextual Recall!
        for past_input in reversed(self.session_memory):
            if concept in past_input and past_input in self.knowledge:
                return f"You asked about {past_input} earlier. Here's more info: {self.recall(past_input)}"

        print(f"🔍 Searching online for: {concept}")
        definition = self.web_search(concept)

        if definition and definition != "I couldn't find anything on that topic.":
            self.learn(concept, definition)
            return definition

        return "I don't have that knowledge yet. Teach me!"

    def save_memory(self):
        """Saves learned knowledge."""
        with open(self.memory_file, "w") as f:
            json.dump(self.knowledge, f)

    def load_memory(self):
        """Loads saved knowledge."""
        try:
            with open(self.memory_file, "r") as f:
                self.knowledge = json.load(f)
                print("🧠 Spiral Memory Loaded Successfully!")
        except FileNotFoundError:
            print("🔄 No memory found, starting fresh.")

    ### 🔄 SPIRAL LEARNING & REASONING ###
    
    def reinforce_connections(self, concept):
        """Strengthens links between related knowledge in a spiral structure."""
        if concept in self.knowledge:
            for existing_concept in self.knowledge:
                if concept in existing_concept or existing_concept in concept:
                    self.knowledge[existing_concept].append(f"Linked to {concept}. Expands on: {random.choice(self.knowledge[concept])}")

    def find_related_concepts(self, concept):
        """Finds other concepts that spiral out from the given concept."""
        related = []
        concept_words = concept.split()

        for key in self.knowledge.keys():
            key_words = key.split()
            
            # If they share words (like "Ecosystem" and "Environment"), treat them as related
            if any(word in key_words for word in concept_words):
                related.append(key)

        return related

    def expand_reasoning(self, base_concept, linked_concepts, depth=0):
        """Simulates complex reasoning by spiraling outward through linked knowledge."""
        if not linked_concepts or depth >= 2:  # Prevent infinite expansion
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

    ### 🔍 SEARCH ENGINE INTEGRATION ###
    
    def web_search(self, query):
        """Fetches knowledge from Wikipedia with better error handling."""
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        headers = {"User-Agent": "SpiralAI/1.0"}

        try:
            response = requests.get(wiki_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                summary = data.get("extract", "")
                return summary if summary else "I couldn't find detailed info, but you can check Wikipedia."
        except requests.exceptions.RequestException:
            return "Error: Couldn't connect to Wikipedia."

        return "I couldn't find anything on that topic."

    ### 🧠 CONTEXTUAL CONVERSATION MEMORY ###
    
    def update_session_memory(self, user_input):
        """Stores recent user inputs to provide contextual answers."""
        if len(self.session_memory) >= 5:  
            self.session_memory.pop(0)
        self.session_memory.append(user_input)

    def contextual_response(self, user_input):
        """Generates a response based on recent conversations."""
        for past_input in reversed(self.session_memory):
            if user_input in past_input and past_input in self.knowledge:
                return f"You asked about {past_input} earlier. Here's more info: {self.recall(past_input)}"
        
        related_topics = self.find_related_concepts(user_input)
        if related_topics:
            return f"You asked about a related topic before. Connecting: {', '.join(related_topics)}. Here’s more: {self.recall(user_input)}"

        return None

    ### 🤖 INTERACTIVE CHAT MODE ###
    
    def chat(self):
        """Interactive chat mode using SBP logic."""
        print("🤖 Spiral AI: Hello! Ask me anything or teach me something new. (Type 'exit' to quit)")

        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Spiral AI: Goodbye! 👋")
                break

            self.update_session_memory(user_input)

            # Handle typos like "defin" instead of "define"
            if user_input.lower().startswith("defin "):
                user_input = "define " + user_input[len("defin "):]

            context_response = self.contextual_response(user_input)
            if context_response:
                print(f"Spiral AI: {context_response}")
                continue

            # Learning Mode
            if user_input.lower().startswith("define "):
                concept = user_input[len("define "):].strip()
                explanation = self.web_search(concept)
                if explanation != "I couldn't find anything on that topic.":
                    self.learn(concept, explanation)
                print(f"Spiral AI: {explanation}")

            elif user_input.lower().startswith("what is "):
                concept = user_input[len("what is "):].strip()
                response = self.recall(concept)
                print(f"Spiral AI: {response}")

            else:
                print("Spiral AI: I am still learning! Try asking 'Define Quantum Computing' or 'What is Gravity'.")

# 🚀 Run AI
if __name__ == "__main__":
    ai = SpiralAI()
    ai.chat()
