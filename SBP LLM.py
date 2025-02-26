pip install nltk
import random
import nltk
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import words

nltk.download("punkt")
nltk.download("words")

# 🔥 SBP LLM - Learning Without Pretraining
class SpiralLanguageAI:
    def __init__(self, base_vocab=None, adaptability=0.05):
        """Initializes SBP LLM with a base vocabulary and self-learning mechanism."""
        self.growth_factor = random.uniform(1.1, 1.3)  # Expands linguistic learning dynamically
        self.adaptability = adaptability
        self.memory = []
        self.last_update = datetime.now()
        self.vocabulary = base_vocab if base_vocab else ["Hello", "world", "AI", "learning"]
        self.sentences = []

    def next_value(self):
        """Expands AI's language ability dynamically based on interaction."""
        time_elapsed = (datetime.now() - self.last_update).total_seconds()
        self.growth_factor += self.adaptability * random.uniform(-0.05, 0.05)
        self.memory.append(self.growth_factor)
        self.memory = self.memory[-5:]  # Keeps last 5 learning states
        self.last_update = datetime.now()
        return self.growth_factor

    def learn_from_sentence(self, sentence):
        """AI expands vocabulary and learning based on new sentences."""
        words_in_sentence = word_tokenize(sentence)
        for word in words_in_sentence:
            if word.lower() not in self.vocabulary and word.lower() in words.words():
                self.vocabulary.append(word.lower())
        self.sentences.append(sentence)

    def generate_sentence(self):
        """Creates new sentences dynamically using learned vocabulary."""
        if len(self.vocabulary) < 5:
            return "Learning in progress..."
        sentence_length = random.randint(4, 10)
        sentence = " ".join(random.choices(self.vocabulary, k=sentence_length))
        return sentence.capitalize() + "."

# 🔥 Run SBP-Based LLM Without Pretraining
if __name__ == "__main__":
    sbp_llm = SpiralLanguageAI()

    print("\n🔵 **SBP AI is now learning... Provide it with sentences!**")

    while True:
        user_input = input("\n📝 Enter a sentence to teach SBP AI: ")
        sbp_llm.learn_from_sentence(user_input)
        print("✅ SBP AI has learned! Generating a sentence...")
        
        ai_sentence = sbp_llm.generate_sentence()
        print(f"\n🤖 AI Says: {ai_sentence}")