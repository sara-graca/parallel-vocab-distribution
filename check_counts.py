import json
from collections import Counter

sequential = Counter(json.load(open("results/counts_sequential.json")))
threads_static = Counter(json.load(open("results/counts_threads_static.json")))
threads_queue = Counter(json.load(open("results/counts_threads_queue.json")))
joblib_counts = Counter(json.load(open("results/counts_joblib.json")))
mp_counts = Counter(json.load(open("results/counts_multiprocessing.json")))

print(f"Sequential == Threads static:  {sequential == threads_static}")
print(f"Sequential == Threads queue:   {sequential == threads_queue}")
print(f"Sequential == Joblib:          {sequential == joblib_counts}")
print(f"Sequential == Multiprocessing: {sequential == mp_counts}")