import subprocess
import os

experiment_scripts = [
    "sequential.py",
    "threads_static.py",
    "threads_dynamic.py",
]

process_scripts = [
    "joblib_parallel.py",
    "mp_parallel.py",
]

num_runs = 100

for script in experiment_scripts:
    print(f"Running {script} {num_runs} times...")
    for i in range(1, num_runs+1):
        subprocess.run(["python", script], check=True)

for jobs in ["2", "4", "8"]:
    os.environ["N_JOBS"] = jobs
    print(f"Running joblib_parallel.py {num_runs} times with {jobs} jobs...")
    for i in range(1, num_runs+1):
        subprocess.run(["python", "joblib_parallel.py"], check=True)

for workers in ["2", "4", "8"]:
    os.environ["N_WORKERS"] = workers
    print(f"Running mp_parallel.py {num_runs} times with {workers} workers...")
    for i in range(1, num_runs+1):
        subprocess.run(["python", "mp_parallel.py"], check=True)