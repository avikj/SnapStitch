# clustering.py

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import pickle

# input: embeddings for every frame
# X =

def db_scan(X, eps=1, min_pts=30):
  db = DBSCAN(eps=eps, min_samples=min_pts).fit(X)

  # array of booleans, true representing a core point
  core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  labels = db.labels_
  # print labels
  # Number of clusters in labels, ignoring noise if present.
  n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0) 
  with open('labels_eps%d_minpts%d.tsv'%(eps, min_pts), 'w') as outfile:
    for label in labels:
      outfile.write('%d\n'%label)

  print n_clusters_

def get_clusters_from_frames(frame_dir=None):
  
  # TODO: allow multiple frame directories to be processed at once
  if frame_dir is None:
    filename_to_embedding = pickle.load(open('filename_to_embedding.pkl')) # TODO: call get_inception_embeddings on frame dir, but for now just use the pickle
    embs = []
    filenames = []
    for filename, embedding in filename_to_embedding.iteritems():
      embs.append(embedding)
      filenames.append(filename)
    embs = np.array(embs)
    candidates = [(11, 6)]
    candidates = [(eps, min_pts) for eps in range(7, 15) for min_pts in range(2, 10)]
    for eps, min_pts in candidates:
        print eps, min_pts
        db_scan(embs, eps=eps, min_pts=min_pts)
        print ''
# sample data
'''
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)
'''

# X = StandardScaler().fit_transform(X)

#db_scan(X)

if __name__ == '__main__':
  get_clusters_from_frames()