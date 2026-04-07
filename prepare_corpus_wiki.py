import os
import re
from datasets import load_dataset

OUTPUT_DIR = "data/"
N_ARTICLES = 500

os.makedirs(OUTPUT_DIR, exist_ok=True)

dataset = load_dataset("wikitext", "wikitext-103-raw-v1", split="train")

articles = []
current = []

for line in dataset["text"]:
    if re.match(r" = [^=]", line) and current:
        articles.append("".join(current).strip())
        current = [line]
    else:
        current.append(line)

if current:
    articles.append("".join(current).strip())

articles = [a for a in articles if len(a) > 200][:N_ARTICLES]

for i, article in enumerate(articles):
    path = os.path.join(OUTPUT_DIR, f"wiki_{i:04d}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(article)
    size_kb = os.path.getsize(path) // 1024

print(f"\nDone! {len(articles)} articles saved to '{OUTPUT_DIR}'")