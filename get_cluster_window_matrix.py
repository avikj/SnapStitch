# get_cluster_window_matrix.py
import numpy as np
import pickle

FRAME_PATH = '/frames/...'
SLIDING_WINDOW_SIZE = 30

# cluster_filename = 'test.pickle'
# t = (2, {'frame1.jpg':0,'frame2.jpg':0,'frame3.jpg':1,'frame4.jpg':1})

with open(cluster_filename, 'wb') as stream:
	pickle.dump(t, stream)

def get_filenames_to_clusters(filename):
	with open(filename, 'rb') as stream:
		data = pickle.load(stream)
	return data

# returns dictionary with keys of cluster numbers and values of frames
def get_cluster_to_filenames(filenames_to_cluster):
	num_clusts = np.max(np.array([clust for clust in filenames_to_cluster.values()])) + 1
	cluster_to_filenames = {k:[] for k in range(num_clusts)}
	for frame, clust in filenames_to_cluster.iteritems():
		if clust == -1: continue
		cluster_to_filenames[clust].append(frame)
	return cluster_to_filenames

def get_frame_vector(frame):
	path = FRAME_PATH + frame + '.npy'
	return np.load(path)

def get_centroid(cluster):
	clust_points = np.array([get_frame_vector(frame) for frame in clust])
	assert(clust_points.shape[0] == len(cluster) and clust_points[1] == 2048)
	centroid = np.mean(clust_points, axis=0)
	return centroid

def get_avg_error(window, centroid):
	frames = np.array([get_frame_vector(frame) for frame in window])
	assert(frames.shape[0] == len(window) and frames.shape[1] == 2048)
	diffs = frames - centroid
	errors = np.linalg.norm(diffs, ord=2, axis=1)
	avg_error = np.mean(dists)
	return avg_error
	
def get_best_windows(cluster_to_filenames):
	# compute matrix of window vs. cluster
	win_clust_vecs = []
	for clust in cluster_to_filenames.keys():
		filenames = cluster_to_filenames[clust]
		centroid = get_centroid(filenames)
		file_windows = [filenames[i:i+SLIDING_WINDOW_SIZE] for i in xrange(len(filenames)-SLIDING_WINDOW_SIZE+1)]
		clust_errors = np.array([get_avg_error(window, centroid) for window in file_windows])
		win_clust_vecs.append(clust_errors)
	win_clust_mat = np.vstack(np.array(win_clust_vecs))
	assert(win_clust_mat.shape[1] == len(cluster_to_filenames.keys()))

	# find best index of best window
	best_wins = np.argmax(win_clust_mat, axis=0)
	return best_wins


# get clustered frames
filenames_to_cluster = get_filenames_to_clusters(cluster_filename)
cluster_to_filenames = get_cluster_to_filenames(filenames_to_cluster)

# get best windows
best_wins = get_best_windows(cluster_to_filenames)