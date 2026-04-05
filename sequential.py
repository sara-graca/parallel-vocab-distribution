import os
import re
import time
import csv
from collections import Counter


DATA_DIR = "data/"
RESULTS_FILE = "results/timing.csv"

filepaths = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)])

# read
t0 = time.perf_counter()
texts = []
for fp in filepaths:
    with open(fp, "r", encoding="utf-8") as f:
        texts.append(f.read())
read_time = time.perf_counter() - t0

# tokenize
t0 = time.perf_counter()
tokenized = [re.findall(r"[a-z]+", text.lower()) for text in texts]
tokenize_time = time.perf_counter() - t0

# count locally
t0 = time.perf_counter()
partial_counts = [Counter(tokens) for tokens in tokenized]
count_time = time.perf_counter() - t0

# merge
t0 = time.perf_counter()
global_counts = Counter()
for counter in partial_counts:
    global_counts.update(counter)
merge_time = time.perf_counter() - t0

total = read_time + tokenize_time + count_time + merge_time

print(f"Read:     {read_time:.4f}s")
print(f"Tokenize: {tokenize_time:.4f}s")
print(f"Count:    {count_time:.4f}s")
print(f"Merge:    {merge_time:.4f}s")
print(f"Total:    {total:.4f}s")
print(f"\nUnique words: {len(global_counts)}")
print(f"Total tokens: {sum(global_counts.values())}")
print(f"\nTop 10:")
for word, count in global_counts.most_common(10):
    print(f"  {word:<15} {count}")


# save results 

file_exists = os.path.exists(RESULTS_FILE)
with open(RESULTS_FILE, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["version", "read", "tokenize", "count", "merge", "total"])
    if not file_exists:
        writer.writeheader()
    writer.writerow({
    "version": "sequential",
    "read": round(read_time, 4),
    "tokenize": round(tokenize_time, 4),
    "count": round(count_time, 4),
    "merge": round(merge_time, 4),
    "total": round(total, 4)
})
 
print(f"\nResults saved to {RESULTS_FILE}")