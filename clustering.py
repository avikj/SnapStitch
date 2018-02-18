# clustering.py
import errno
from shutil import copy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pickle
import os
import pprint
# input: embeddings for every frame
# X =

def cluster(X, eps=1, min_pts=30, algorithm='DBSCAN', n_clusters=10):
  if algorithm == 'DBSCAN':
    cluster_result = DBSCAN(eps=eps, min_samples=min_pts).fit(X)
  elif algorithm == 'KMeans':
    cluster_result = KMeans(n_clusters=n_clusters).fit(X)
  labels = cluster_result.labels_
  print labels
  return labels

def get_clusters_for_project(project_id, video_names):
  embs = []
  filenames = []
  for video_name in video_names:
    filename_to_embedding = pickle.load(open(os.path.join('temp', project_id, video_name, 'filename_to_emb.pkl'))) # TODO: call get_inception_embeddings on frame dir, but for now just use the pickle
    for filename, embedding in filename_to_embedding.iteritems():
      embs.append(embedding)
      filenames.append(filename)
  labels = cluster(embs, algorithm='KMeans', n_clusters=10)
  d = {}
  for video_name in video_names:
    d[video_name] = {}
  for i in range(len(filenames)):
    video_name = video_name_from_filename(filenames[i])
    d[video_name][filenames[i]] = labels[i]
  with open(os.path.join('temp', project_id, 'filename_to_clust.pkl'), 'w') as pickle_file:
    pickle.dump(d, pickle_file)
  for video_name in d:
    for filename in d[video_name]:
      mkdir_p(os.path.join('temp', project_id, 'clusters', str(d[video_name][filename])))
      copy(filename, os.path.join('temp', project_id, 'clusters', str(d[video_name][filename]), os.path.basename(filename)))
  '''filenames = [filename[filename.rindex('/')+1:] for filename in filenames]
  embs = np.array(embs)
  candidates = [(11, 6)]
  candidates = [(eps, min_pts) for eps in range(7, 15) for min_pts in range(2, 10)]'''

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise  
def get_clusters_from_frames(frame_dir=None):
  
  # TODO: allow multiple frame directories to be processed at once
  if frame_dir is None:
    filename_to_embedding = pickle.load(open('temp/temp_vid1_290717183249/filename_to_emb.pkl')) # TODO: call get_inception_embeddings on frame dir, but for now just use the pickle
    embs = []
    filenames = []
    for filename, embedding in filename_to_embedding.iteritems():
      embs.append(embedding)
      filenames.append(filename)
    filenames = [filename[filename.rindex('/')+1:] for filename in filenames]
    embs = np.array(embs)
    candidates = [(11, 6)]
    candidates = [(eps, min_pts) for eps in range(7, 15) for min_pts in range(2, 10)]
    reduced = PCA().fit(embs).transform(embs)
    labels = cluster(embs, filenames, algorithm='KMeans', n_clusters=10)

def video_name_from_filename(img_filename):
  return img_filename.split('/')[-3]
    # cluster(embs, filenames, n_clusters_=6)
# sample data
'''
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)
'''

# X = StandardScaler().fit_transform(X)

#cluster(X)

if __name__ == '__main__':
  pp = pprint.PrettyPrinter(indent=4)
  d = get_clusters_for_project('1234', ['vid1', 'vid2'])
  pp.pprint(d)
