# Parallel Vocabulary Distribution
 
Profiling Python and parallel word counting using a MapReduce approach. Compares sequential, thread-based, and process-based implementations on a combined corpus of 18 Gutenberg books and 500 Wikipedia articles.
 
## Corpus
 
```bash
python prepare_corpus.py        # downloads NLTK Gutenberg corpus
python prepare_corpus_wiki.py   # downloads 500 wikitext-103 articles
```
 
## Running experiments
 
```bash
python sequential.py
python threads_static.py
python threads_dynamic.py
python joblib_parallel.py
python mp_parallel.py
```
 
Results are appended to `results/timing.csv` after each run.
 
## Verify correctness
 
```bash
python check_counts.py
```
 
## Plot results
 
```bash
python plot.py
```
 
Saves a bar chart to `results/total_runtime.png`.
 
## Data versioning
 
Data and results are tracked with DVC. After running experiments:
 
```bash
dvc add data/ results/
git add data.dvc results.dvc
git commit -m "update results"
```
 
