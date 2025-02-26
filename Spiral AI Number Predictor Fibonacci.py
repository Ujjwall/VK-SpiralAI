import numpy as np

class SpiralAI:
    def __init__(self, memory_size=5):
        self.memory_size = memory_size
        self.memory = []  # Stores past numbers in a spiral-learning fashion

    def update_memory(self, number):
        """Updates memory by keeping recent but relevant past values."""
        self.memory.append(number)
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)  # Keep last values but remove the oldest

    def predict_next(self):
        """Predicts the next number based on Fibonacci pattern, strictly enforcing sum rule."""
        
        # 🚀 Handle first few inputs correctly
        if len(self.memory) == 0:
            return 0  # If no input, return 0
        elif len(self.memory) == 1:
            return self.memory[-1]  # If only one number, return itself
        elif len(self.memory) == 2:
            return self.memory[-1] + self.memory[-2]  # Strictly use Fibonacci sum

        # 🚀 Enforce Fibonacci rule for all cases
        return self.memory[-1] + self.memory[-2]  # Always sum last two numbers

def main():
    ai = SpiralAI(memory_size=5)
    
    print("Spiral AI: Enter numbers to train me. Type 'exit' to stop.")

    while True:
        user_input = input("Enter a number (or type 'exit'): ")
        if user_input.lower() == 'exit':
            break
        try:
            number = int(user_input)
            prediction = ai.predict_next()
            print(f"Prediction: {prediction}")
            ai.update_memory(number)
        except ValueError:
            print("Please enter a valid number.")

    # 🚀 **Auto-predict Fibonacci sequence after user stops entering values**
    print("\nGenerating next Fibonacci numbers:")
    for _ in range(5):  # Generate 5 more Fibonacci numbers
        prediction = ai.predict_next()
        print(f"Next Fibonacci Number: {prediction}")
        ai.update_memory(prediction)

if __name__ == "__main__":
    main()
