"""
Code Name: lm_long_text_benchmark
File: issues/issue_759_lm_performance_test.py

This script tests LM Studio's performance (latency and memory usage)
on long text inputs (10-20 pages).
"""

import time
import tracemalloc
from lm_studio import LMModel  # فرض بر این است که LM Studio API به این صورت import می‌شود

# Initialize LM Studio model
model = LMModel()

# Example: a long text (10-20 pages)
with open("long_text_sample.txt", "r", encoding="utf-8") as f:
    long_text = f.read()

# Start memory tracking
tracemalloc.start()

# Start timing
start_time = time.time()

# Generate response from LM Studio
response = model.generate(long_text)

# End timing
end_time = time.time()
elapsed_time = end_time - start_time

# Measure memory usage
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"LM Studio response length: {len(response)} characters")
print(f"Elapsed time: {elapsed_time:.2f} seconds")
print(f"Memory usage: Current = {current / 1024 / 1024:.2f} MB; Peak = {peak / 1024 / 1024:.2f} MB")
