import math
import numpy as np
import random
from datetime import datetime

class SpiralAI:
    """
    Spiral-Based AI Model: A lightweight, real-time learning AI.
    Uses a self-evolving spiral function to generate and adapt its intelligence dynamically.
    """

    def __init__(self, start=1, growth_factor=math.e, memory_limit=10, adaptability=0.1):
        """
        Initialize SpiralAI with dynamic memory expansion.
        :param start: Initial value of the AI state.
        :param growth_factor: The base for exponential learning (default: Euler's number).
        :param memory_limit: Number of past states to retain.
        :param adaptability: The rate at which AI adjusts to new inputs.
        """
        self.position = start
        self.growth_factor = growth_factor
        self.memory = []
        self.memory_limit = memory_limit
        self.adaptability = adaptability
        self.last_update = datetime.now()

    def next_value(self):
        """
        Generates the next step in the spiral-based learning model.
        It evolves dynamically instead of running in static loops.
        """
        time_elapsed = (datetime.now() - self.last_update).total_seconds()
        self.position *= self.growth_factor + (self.adaptability * random.uniform(-0.1, 0.1))
        self.memory.append(self.position)
        self.manage_memory()
        self.last_update = datetime.now()
        return self.position

    def manage_memory(self):
        """
        Manages memory retention by removing outdated values.
        Ensures AI remains adaptive while reducing unnecessary data storage.
        """
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

    def adjust_growth_factor(self, external_input):
        """
        Dynamically adjusts the growth factor based on real-time external data.
        This enables adaptive learning in response to new information.
        """
        self.growth_factor += external_input * self.adaptability

    def get_memory(self):
        """
        Returns stored memory states for external applications.
        """
        return self.memory

    def reset(self, start=1):
        """
        Resets the AI to its initial state for testing and new implementations.
        """
        self.position = start
        self.memory = []

# Example Usage:
if __name__ == "__main__":
    spiral_ai = SpiralAI(start=1)

    print("Running Spiral AI Model...")
    for _ in range(10):
        print(f"Spiral AI Step: {spiral_ai.next_value()}")

    print("Spiral AI Model Successfully Running!")
