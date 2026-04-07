import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/timing.csv")

df["total"] = pd.to_numeric(df["total"], errors="coerce")
df = df[~((df["version"] == "sequential") & (df["total"] > 5))]

summary = df.groupby("version")["total"].agg(["mean", "std"]).reset_index()

summary = summary.sort_values("mean")

plt.figure()

plt.bar(summary["version"], summary["mean"], yerr=summary["std"])

plt.xticks(rotation=45, fontsize=8)
plt.xlabel("Method")
plt.ylabel("Total Time (s)")
plt.title("Average Runtime by Implementation")

plt.tight_layout()

plt.savefig("results/total_runtime.png", dpi=300)
plt.show()