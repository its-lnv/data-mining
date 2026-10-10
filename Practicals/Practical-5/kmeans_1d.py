import random
import numpy as np

# ------------------------------------------------
# Generate 20 random 1-D points
# ------------------------------------------------

random.seed(42)

points = [random.randint(1, 100) for _ in range(20)]

print("20 RANDOM 1-D POINTS")
print(points)


# ------------------------------------------------
# Ask user for value of k
# ------------------------------------------------

k = int(input("\nEnter value of k: "))

if k <= 0 or k > len(points):
    print("Invalid value of k.")
    exit()


# Convert points into numpy array
points = np.array(points, dtype=float)


# ------------------------------------------------
# Select initial centroids
# ------------------------------------------------

centroids = np.array(
    random.sample(list(points), k),
    dtype=float
)

print("\nInitial Centroids:")
print(centroids)


# ------------------------------------------------
# K-Means Algorithm
# ------------------------------------------------

max_iterations = 100

for iteration in range(max_iterations):

    # Calculate distance of every point
    # from every centroid
    distances = np.abs(
        points[:, np.newaxis] - centroids
    )

    # Assign each point to nearest centroid
    clusters = np.argmin(distances, axis=1)

    # Store old centroids
    old_centroids = centroids.copy()

    # Calculate new centroids
    for i in range(k):

        cluster_points = points[clusters == i]

        if len(cluster_points) > 0:
            centroids[i] = np.mean(cluster_points)

    # Check convergence
    if np.allclose(old_centroids, centroids):
        break


# ------------------------------------------------
# Display Final Clusters
# ------------------------------------------------

print("\nFINAL CLUSTERS")

for i in range(k):

    cluster_points = points[clusters == i]

    print(
        "Cluster", i + 1,
        ":", cluster_points.astype(int).tolist()
    )

    print(
        "Centroid =",
        round(centroids[i], 2)
    )


print("\nNumber of iterations =", iteration + 1)