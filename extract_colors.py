import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from collections import Counter


class ExtractColors:
    def __init__(self, img_file):
        self.img = np.array(Image.open(img_file).convert('RGB')).reshape(-1, 3)

    def extract(self, n_clusters=10):
        kmeans = KMeans(n_clusters=n_clusters, n_init=1, random_state=0).fit(self.img)
        actual_n_clusters = len(np.unique(kmeans.labels_))
        if actual_n_clusters != n_clusters:
            kmeans = KMeans(n_clusters=actual_n_clusters, n_init=1, random_state=0).fit(self.img)

        clusters = kmeans.cluster_centers_

        colors = []
        for cluster in clusters:
            a = "#"
            for i in cluster:
                a += format(int(i), "02x")
            colors.append(a)

        pixels = len(kmeans.labels_)
        cluster_pixels = Counter(kmeans.labels_)

        data = []
        for name in cluster_pixels.most_common():
            name = name[0]
            item = dict()
            item["color"] = colors[name]
            percentage = round(cluster_pixels[name]/pixels * 100, 1)
            item["percentage"] = percentage
            data.append(item)
        return data
