import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =================================================
# DATASET
# =================================================

data = {
    "X": [
        1, 2, 3, 4, 5,
        8, 9, 10, 11, 12,
        20, 21, 22, 23, 24
    ],

    "Y": [
        2, 3, 1, 4, 3,
        8, 9, 7, 10, 9,
        20, 19, 21, 22, 20
    ]
}

df = pd.DataFrame(data)

X = df[["X", "Y"]].values.astype(float)

print("DATASET")
print(df)


# =================================================
# K-MEANS FUNCTION
# =================================================

def kmeans(X, k, max_iterations=100):

    # Select first k points as initial centroids
    centroids = X[:k].copy()

    mse_history = []

    for iteration in range(max_iterations):

        # -----------------------------------------
        # Calculate distances
        # -----------------------------------------

        distances = np.zeros(
            (len(X), k)
        )

        for i in range(k):

            distances[:, i] = np.sqrt(
                np.sum(
                    (X - centroids[i]) ** 2,
                    axis=1
                )
            )

        # -----------------------------------------
        # Assign clusters
        # -----------------------------------------

        clusters = np.argmin(
            distances,
            axis=1
        )

        # -----------------------------------------
        # Calculate MSE
        # -----------------------------------------

        squared_error = 0

        for i in range(k):

            cluster_points = X[
                clusters == i
            ]

            if len(cluster_points) > 0:

                squared_error += np.sum(
                    (cluster_points - centroids[i]) ** 2
                )

        mse = squared_error / len(X)

        mse_history.append(mse)

        # -----------------------------------------
        # Calculate new centroids
        # -----------------------------------------

        new_centroids = centroids.copy()

        for i in range(k):

            cluster_points = X[
                clusters == i
            ]

            if len(cluster_points) > 0:

                new_centroids[i] = np.mean(
                    cluster_points,
                    axis=0
                )

        # -----------------------------------------
        # Check convergence
        # -----------------------------------------

        if np.allclose(
            centroids,
            new_centroids
        ):
            centroids = new_centroids
            break

        centroids = new_centroids

    return clusters, centroids, mse_history


# =================================================
# RUN K-MEANS FOR DIFFERENT VALUES OF K
# =================================================

results = {}

for k in [2, 3, 4]:

    clusters, centroids, mse_history = kmeans(
        X,
        k
    )

    results[k] = {
        "clusters": clusters,
        "centroids": centroids,
        "mse": mse_history
    }


# =================================================
# DISPLAY RESULTS
# =================================================

print("\n======================================")
print("K-MEANS RESULTS")
print("======================================")


for k in results:

    print("\nK =", k)

    print(
        "Number of iterations =",
        len(results[k]["mse"])
    )

    print(
        "Final MSE =",
        round(
            results[k]["mse"][-1],
            2
        )
    )

    print(
        "Centroids:"
    )

    print(
        np.round(
            results[k]["centroids"],
            2
        )
    )


# =================================================
# MSE AFTER EACH ITERATION
# =================================================

print("\n======================================")
print("MSE AFTER EACH ITERATION")
print("======================================")


for k in results:

    print("\nK =", k)

    for i, mse in enumerate(
        results[k]["mse"]
    ):

        print(
            "Iteration",
            i + 1,
            ": MSE =",
            round(mse, 2)
        )


# =================================================
# PLOT MSE GRAPH
# =================================================

plt.figure(figsize=(8, 5))

for k in results:

    mse_values = results[k]["mse"]

    iterations = range(
        1,
        len(mse_values) + 1
    )

    plt.plot(
        iterations,
        mse_values,
        marker="o",
        label=f"k = {k}"
    )


plt.xlabel("Iteration")
plt.ylabel("MSE")
plt.title("MSE after Each K-Means Iteration")

plt.legend()
plt.grid(True)

plt.show()