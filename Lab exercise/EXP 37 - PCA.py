
# Dimensionality Reduction using PCA

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Step 1: Load the Iris dataset
data = load_iris()
X = data.data

print("Original Dataset Shape:", X.shape)

# Step 2: Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Step 4: Display reduced dataset
print("\nReduced Dataset Shape:", X_pca.shape)

print("\nFirst 5 Rows of Reduced Data:")
print(X_pca[:5])

# Step 5: Display explained variance
print("\nExplained Variance Ratio:")
print(pca.explained_variance_ratio_)

print("\nTotal Variance Retained:",
      sum(pca.explained_variance_ratio_) * 100, "%")
