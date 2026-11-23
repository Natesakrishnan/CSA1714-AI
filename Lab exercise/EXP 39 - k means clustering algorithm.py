
# Clustering using K-Means Algorithm

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Step 1: Generate sample data
X, y = make_blobs(
    n_samples=100,
    centers=3,
    cluster_std=1.0,
    random_state=42
)

# Step 2: Apply K-Means clustering
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

kmeans.fit(X)

# Step 3: Get cluster labels and centroids
labels = kmeans.labels_
centroids = kmeans.cluster_centers_

# Step 4: Display results
print("Cluster Labels:")
print(labels)

print("\nCluster Centroids:")
print(centroids)

print("\nNumber of Clusters:", kmeans.n_clusters)

# Step 5: Visualize the clusters
plt.scatter(
    X[:, 0], X[:, 1],
    c=labels,
    cmap='viridis',
    s=50
)

plt.scatter(
    centroids[:, 0], centroids[:, 1],
    color='red',
    marker='X',
    s=200,
    label='Centroids'
)

plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()
