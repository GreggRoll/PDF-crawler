import json
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def vectorize_text(json_objects):
    """ Convert text content of JSON objects to a vectorized form. """
    # Join the list of strings into a single string for each JSON object
    text_data = [" ".join(obj["content"]) for obj in json_objects]
    vectorizer = TfidfVectorizer()
    return vectorizer.fit_transform(text_data)

def visualize_clusters(features, labels, filenames):
    """ Visualize the clusters using PCA for dimensionality reduction. """
    # Reduce dimensions to 2D
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(features.toarray())

    # Scatter plot with annotations
    plt.figure(figsize=(12, 8))
    for i, (x, y) in enumerate(reduced_features):
        plt.scatter(x, y, c=labels[i], cmap='viridis')
        plt.text(x, y, filenames[i][5:], fontsize=9)

    plt.title("Cluster Visualization with Filenames")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.colorbar(label='Cluster Label')
    plt.show()

def cluster(json_objects):
    # Vectorize text content
    features = vectorize_text(json_objects)

    # Perform clustering
    n_clusters = 5  # Adjust as needed
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(features)

    # Filenames for annotation
    filenames = [obj["filename"] for obj in json_objects]

    # Visualize
    return visualize_clusters(features, labels, filenames)

# # Load JSON data
# with open("output.json") as f:
#     json_objects = json.load(f)

# cluster(json_objects)