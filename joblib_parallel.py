import os
import re
import time
import csv
from collections import Counter
import joblib


DATA_DIR = "data/"
RESULTS_FILE = "results/timing.csv"
N_JOBS = int(os.getenv("N_JOBS", 4))

filepaths = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)])

def process_file(fp):
    with open(fp, "r", encoding="utf-8") as f:
        text = f.read()
    tokens = re.findall(r"[a-z]+", text.lower())
    return Counter(tokens)

# map
t0 = time.perf_counter()
partial_counts = joblib.Parallel(n_jobs=N_JOBS)(joblib.delayed(process_file)(fp) for fp in filepaths)
map_time = time.perf_counter() - t0

# merge
t0 = time.perf_counter()
global_counts = Counter()
for counter in partial_counts:
    global_counts.update(counter)
merge_time = time.perf_counter() - t0

total = map_time + merge_time

print(f"Map:   {map_time:.4f}s")
print(f"Merge: {merge_time:.4f}s")
print(f"Total: {total:.4f}s")
print(f"\nUnique words: {len(global_counts)}")
print(f"Total tokens: {sum(global_counts.values())}")

file_exists = os.path.exists(RESULTS_FILE)
with open(RESULTS_FILE, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["version", "read", "tokenize", "count", "merge", "total"])
    if not file_exists:
        writer.writeheader()
    writer.writerow({
        "version": f"joblib_{N_JOBS}",
        "read": "N/A",
        "tokenize": "N/A",
        "count": "N/A",
        "merge": round(merge_time, 4),
        "total": round(total, 4)
    })

print(f"\nResults saved to {RESULTS_FILE}")

import json
json.dump(dict(global_counts), open("results/counts_joblib.json", "w"))