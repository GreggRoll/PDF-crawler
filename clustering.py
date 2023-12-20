import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.cluster import KMeans

#vectorize json structure
def extract_features(json_objects):
    """ Extract features from JSON objects. """
    vectorizer = DictVectorizer(sparse=False)
    return vectorizer.fit_transform(json_objects)

#cluster based on json features
def cluster_json_objects(json_objects, n_clusters=2):
    """ Cluster JSON objects based on their structure. """
    # Extract features
    features = extract_features(json_objects)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(features)

    # Return cluster labels
    return kmeans.labels_

# with open("output.json") as f:
#     json_objects = json.load(f)

# cluster_json_objects(json_objects)