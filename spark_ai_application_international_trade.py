from pyspark.sql import SparkSession
import math
import random

spark = SparkSession.builder \
    .appName("SpiralTradeOptimizer") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

class TradeRouteOptimizer:
    def __init__(self, start_cost=1000, demand_factor=math.e, memory_limit=1000):
        self.current_cost = start_cost
        self.demand_factor = demand_factor
        self.memory = []
        self.memory_limit = memory_limit

    def next_route(self):
        fluctuation = random.uniform(0.9, 1.1)
        self.current_cost *= (self.demand_factor * fluctuation)
        self.memory.append(self.current_cost)
        self.manage_memory()
        return self.current_cost

    def manage_memory(self):
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

def run_trade_optimizer(index):
    trade_ai = TradeRouteOptimizer(start_cost=index * 1000)
    return [trade_ai.next_route() for _ in range(100)]

num_nodes = 10  # 10 parallel trade simulations
rdd = spark.sparkContext.parallelize(range(1, num_nodes + 1))
results = rdd.map(run_trade_optimizer).collect()

for idx, res in enumerate(results):
    print(f"Trade Simulation {idx + 1}: {res[:5]}...")

spark.stop()