from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



class Predictor:
    def __init__(self,df):
        self.df=df
        self.resistances=np.array([])
        self.supports=np.array([])
        self.model=None


    def predict_support(self,lows):

        low_clusters = self.get_optimum_clusters(lows)
        low_centers = low_clusters.cluster_centers_
        low_centers = np.sort(low_centers, axis=0)

        self.supports= low_centers


    def predict_resistance(self,highs):

        high_clusters = self.get_optimum_clusters(highs)
        high_centers = high_clusters.cluster_centers_
        high_centers = np.sort(high_centers, axis=0)

        self.resistances= high_centers

    def get_optimum_clusters(self,df,saturation_point=0.05):

        wcss = []
        k_models = []

        size = min(11, len(df.index))
        for i in range(1, size):
            self.model = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
            self.model.fit(df)
            wcss.append(self.model.inertia_)
            k_models.append(self.model)

    # Compare differences in inertias until it's no more than saturation_point
        optimum_k = len(wcss)-1
        for i in range(0, len(wcss)-1):
            diff = abs(wcss[i+1] - wcss[i])
            if diff < saturation_point:
                optimum_k = i
                break

        print("Optimum K is " + str(optimum_k + 1))
        optimum_clusters = k_models[optimum_k]

        return optimum_clusters
