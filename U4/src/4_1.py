#!/usr/bin/env python3
# coding: utf-8
import numpy as np
import sys

DATA = np.array([
    [3,9,9,10,6,7,4,4],
    [10,2,4,10,6,9,5,3],
    [1,3,1,3,8,1,1,5]
]).T


def expectation(data, centers):
    """
    Assigns datapoints to centers
    """
    clusters = [[] for _ in range(centers.shape[0])]

    for point in data:
            # Calculate distances from centers
            d = np.linalg.norm(centers - point, axis=1)

            # Find the index according to the lowest distance
            id_min = np.argmin(d)
            
            # Assing point to minimum distance
            clusters[id_min].append(point)

    for clt in clusters:
        if len(clt) == 0:
            print("Error: Empty cluster occured, please re-run the program.")
            sys.exit(1)
    return clusters


def minimization(clusters):
    """
    Computes new cluster means
    """
    centers = [np.mean(cls, axis=0) for cls in clusters]

    return np.vstack(centers)


def k_means(data, k, sigma):
    # Initialize with k random points
    centers = data[np.random.randint(data.shape[0], size=k)]
    
    dist = sigma + 1
    while dist > sigma:
        # Assign data points to centers
        clusters = expectation(data, centers)
        
        # Calculate new centers
        new_centers = minimization(clusters)
        
        # Calc maximum center movement
        dist = max(np.linalg.norm(centers - new_centers, axis=1))
        centers = new_centers
                
    return centers, clusters


def print_clusters(centers, clusters):
    for center, clst in zip(centers, clusters):
        print("Center for this Cluster: {}".format(center))
        print("Contains:")
        for _ in clst:
            print(_)
        print()


centers, clusters = k_means(DATA, k=3, sigma=3/4)
print_clusters(centers, clusters)

