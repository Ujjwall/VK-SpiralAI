import math

class SpiralIterator:
    def __init__(self, start=1, growth_factor=math.e, memory_limit=5):
        """Initialize Spiral AI with dynamic memory expansion."""
        self.position = start
        self.growth_factor = growth_factor
        self.memory = []
        self.memory_limit = memory_limit

    def next_value(self):
        """Expands AI learning dynamically instead of in static loops."""
        self.position *= self.growth_factor  
        self.memory.append(self.position)
        self.manage_memory()
        return self.position

    def manage_memory(self):
        """Optimizes memory by removing less relevant data."""
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)  

# Example Usage:
if __name__ == "__main__":
    spiral_ai = SpiralIterator(start=1)
    for _ in range(10):
        print(f"Spiral Expansion Value: {spiral_ai.next_value()}")