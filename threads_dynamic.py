import os
import re
import time
import csv
from collections import Counter
from threading import Thread
from queue import Queue


DATA_DIR = "data/"
RESULTS_FILE = "results/timing.csv"
N_THREADS = 4

filepaths = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR)])

queue = Queue()
for fp in filepaths:
    queue.put(fp)

partial_counts = []

def worker():
    while not queue.empty():
        fp = queue.get()
        print(f"Worker starting: {fp}")
        with open(fp, "r", encoding="utf-8") as f:
            text = f.read()
        tokens = re.findall(r"[a-z]+", text.lower())
        partial_counts.append(Counter(tokens))
        print(f"Worker finished: {fp}")
        queue.task_done()

# map
t0 = time.perf_counter()
threads = [Thread(target=worker) for _ in range(N_THREADS)]
for t in threads: t.start()
for t in threads: t.join()
map_time = time.perf_counter() - t0

# merge
t0 = time.perf_counter()
global_counts = Counter()
for counter in partial_counts:
    global_counts.update(counter)
merge_time = time.perf_counter() - t0

total = map_time + merge_time

print(f"\nMap:   {map_time:.4f}s")
print(f"Merge: {merge_time:.4f}s")
print(f"Total: {total:.4f}s")
print(f"\nUnique words: {len(global_counts)}")
print(f"Total tokens: {sum(global_counts.values())}")
print(f"\nTop 10:")
for word, count in global_counts.most_common(10):
    print(f"  {word:<15} {count}")

file_exists = os.path.exists(RESULTS_FILE)
with open(RESULTS_FILE, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["version", "read", "tokenize", "count", "merge", "total"])
    if not file_exists:
        writer.writeheader()
    writer.writerow({
        "version": f"threads_dyn_{N_THREADS}",
        "read": "N/A",
        "tokenize": "N/A",
        "count": "N/A",
        "merge": round(merge_time, 4),
        "total": round(total, 4)
    })

print(f"\nResults saved to {RESULTS_FILE}")

import json
json.dump(dict(global_counts), open("results/counts_threads_queue.json", "w"))