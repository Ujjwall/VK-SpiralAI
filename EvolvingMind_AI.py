import json
import requests

class MasterAI:
    def __init__(self, memory_file="master_memory.json"):
        self.memory_file = memory_file
        self.knowledge = {}
        self.load_memory()
    
    def learn(self, word, meaning):
        """Learns and stores knowledge permanently."""
        word = word.upper()
        self.knowledge[word] = meaning
        self.save_memory()
        print(f"✅ Learned: {word} - {meaning}")

    def recall(self, word):
        """Retrieves meaning or learns if unknown."""
        word = word.upper()
        
        if word in self.knowledge:
            return self.knowledge[word]
        
        print(f"🔍 Searching online for: {word}")
        definition = self.web_search(word)
        
        if definition and definition != "I couldn't find anything on that topic.":
            self.learn(word, definition)
            return definition
        
        user_definition = input(f"❓ I couldn't find {word}. What does it mean? ")
        if user_definition:
            self.learn(word, user_definition)
            return f"Thanks! I have learned that {word} means: {user_definition}"
        
        return "I couldn't find that word and no one taught me."

    def save_memory(self):
        """Saves learned knowledge."""
        with open(self.memory_file, "w") as f:
            json.dump(self.knowledge, f)

    def load_memory(self):
        """Loads stored knowledge."""
        try:
            with open(self.memory_file, "r") as f:
                self.knowledge = json.load(f)
                print("🧠 Memory Loaded Successfully!")
        except FileNotFoundError:
            print("🔄 No memory found, starting fresh.")

    def web_search(self, query):
        """First tries Wikipedia, then DuckDuckGo if Wikipedia fails."""
        # Wikipedia API
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        headers = {"User-Agent": "MasterAI/1.0 (https://github.com/Ujjwall/VK-SpiralAI)"}

        try:
            response = requests.get(wiki_url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                summary = data.get("extract", "")
                if summary:
                    return summary
        
        except requests.exceptions.RequestException:
            print(f"❌ Wikipedia search failed for: {query}")

        # If Wikipedia fails, try DuckDuckGo
        duck_url = f"https://api.duckduckgo.com/?q={query}&format=json"
        try:
            response = requests.get(duck_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                summary = data.get("AbstractText", "")
                if summary:
                    return summary

        except requests.exceptions.RequestException:
            print(f"❌ DuckDuckGo search failed for: {query}")

        return "I couldn't find anything on that topic."

    def chat(self):
        """Interactive chat mode."""
        print("🤖 Master AI: Hello! Ask me anything or teach me something new.")
        
        while True:
            user_input = input("You: ")
            
            if user_input.lower() in ["exit", "quit"]:
                print("Master AI: Goodbye!")
                break
            
            if "define " in user_input.lower():
                word = user_input.split("define ")[1]
                meaning = self.web_search(word)
                if meaning != "I couldn't find anything on that topic.":
                    self.learn(word, meaning)
                print(f"Master AI: {meaning}")
            
            elif "what is" in user_input.lower():
                word = user_input.split("what is ")[1]
                response = self.recall(word)
                print(f"Master AI: {response}")
            
            else:
                print("Master AI: I am still learning! Try asking 'Define Apple' or 'What is the Sun'.")

# 🚀 Run AI
ai = MasterAI()
ai.chat()

