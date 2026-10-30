from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# Always use the directory containing this Python file.
BASE_DIR = Path(__file__).resolve().parent

# Read the dataset from the same folder as this script.
df = pd.read_csv(BASE_DIR / "iris.csv")

# Use only the four numerical measurements. Species is not a feature.
X = df[
    [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ]
]

# Standardize features because DBSCAN is distance-based.
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Test different DBSCAN parameter values.
eps_values = [0.3, 0.5, 0.7, 1.0]
min_samples_values = [3, 5, 7]

results = []

for eps in eps_values:
    for min_samples in min_samples_values:
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(X_scaled)

        # DBSCAN uses -1 to identify noise points.
        cluster_labels = set(labels) - {-1}
        n_clusters = len(cluster_labels)
        n_noise = int((labels == -1).sum())

        # Calculate silhouette only for non-noise points.
        non_noise_mask = labels != -1
        non_noise_labels = labels[non_noise_mask]
        score = None

        if (
            len(set(non_noise_labels)) >= 2
            and len(set(non_noise_labels)) < len(non_noise_labels)
        ):
            score = silhouette_score(
                X_scaled[non_noise_mask],
                non_noise_labels,
            )

        results.append(
            {
                "eps": eps,
                "min_samples": min_samples,
                "clusters": n_clusters,
                "noise_points": n_noise,
                "noise_percentage": round(
                    n_noise / len(X_scaled) * 100, 2
                ),
                "silhouette_score": score,
            }
        )

        print(
            f"eps={eps}, min_samples={min_samples}, "
            f"clusters={n_clusters}, noise={n_noise}, "
            f"silhouette={score}"
        )

# Save the parameter-comparison results beside this script.
results_df = pd.DataFrame(results)
results_path = BASE_DIR / "dbscan_results.csv"
results_df.to_csv(results_path, index=False)

print("\nDBSCAN Parameter Comparison:")
print(results_df.to_string(index=False))

# Plot the number of clusters for different parameter settings.
plt.figure(figsize=(8, 5))

for min_samples in min_samples_values:
    subset = results_df[results_df["min_samples"] == min_samples]
    plt.plot(
        subset["eps"],
        subset["clusters"],
        marker="o",
        label=f"min_samples={min_samples}",
    )

plt.xlabel("eps")
plt.ylabel("Number of clusters")
plt.title("DBSCAN: Effect of eps and min_samples")
plt.legend()
plt.grid(True)
plt.tight_layout()

plot_path = BASE_DIR / "dbscan_cluster_comparison.png"
plt.savefig(plot_path, dpi=300, bbox_inches="tight")
plt.show()

print("\nFiles created:")
print(f"1. {results_path}")
print(f"2. {plot_path}")
