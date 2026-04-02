import os
import nltk

nltk.download("gutenberg")

from nltk.corpus import gutenberg

OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Gutenberg files: {gutenberg.fileids()}\n")

for filename in gutenberg.fileids():
    text = gutenberg.raw(filename)
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"Saved {filename} ({size_kb} KB)")

print(f"\nDone! {len(gutenberg.fileids())} files saved to '{OUTPUT_DIR}/'")