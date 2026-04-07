import os
import re
import time
import csv
from collections import Counter
from threading import Thread


DATA_DIR = "data/"
RESULTS_FILE = "results/timing.csv"
N_THREADS = len(os.listdir(DATA_DIR))

filepaths = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)])

# read
texts = [None] * len(filepaths)

def read_file(i, fp):
    with open(fp, "r", encoding="utf-8") as f:
        texts[i] = f.read()

t0 = time.perf_counter()
threads = [Thread(target=read_file, args=(i, fp)) for i, fp in enumerate(filepaths)]
for t in threads: t.start()
for t in threads: t.join()
read_time = time.perf_counter() - t0

# tokenize
tokenized = [None] * len(texts)

def tokenize(i, text):
    tokenized[i] = re.findall(r"[a-z]+", text.lower())

t0 = time.perf_counter()
threads = [Thread(target=tokenize, args=(i, text)) for i, text in enumerate(texts)]
for t in threads: t.start()
for t in threads: t.join()
tokenize_time = time.perf_counter() - t0

# count
partial_counts = [None] * len(tokenized)

def count(i, tokens):
    partial_counts[i] = Counter(tokens)

t0 = time.perf_counter()
threads = [Thread(target=count, args=(i, tokens)) for i, tokens in enumerate(tokenized)]
for t in threads: t.start()
for t in threads: t.join()
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

file_exists = os.path.exists(RESULTS_FILE)
with open(RESULTS_FILE, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["version", "read", "tokenize", "count", "merge", "total"])
    if not file_exists:
        writer.writeheader()
    writer.writerow({
        "version": f"threads_static_{N_THREADS}",
        "read": round(read_time, 4),
        "tokenize": round(tokenize_time, 4),
        "count": round(count_time, 4),
        "merge": round(merge_time, 4),
        "total": round(total, 4)
    })

print(f"\nResults saved to {RESULTS_FILE}")

import json
json.dump(dict(global_counts), open("results/counts_threads_static.json", "w"))