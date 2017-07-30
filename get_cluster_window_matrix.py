# get_cluster_window_matrix.py

import numpy as np
import pickle
import sys

def get_clust_to_filename(filename_to_clust):
	num_clusts = max([clust for clust in filename_to_clust.values()]) + 1
	clust_to_filename = {k:[] for k in range(num_clusts)}
	for frame, clust in filename_to_clust.iteritems():
		if clust == -1: continue
		clust_to_filename[clust].append(frame)
	return clust_to_filename

def get_embed(frame_img):
	return np.load(os.path.join(frame_img[:-20], 'embeddings', filename[-14:-4] + '.npy'))

def get_centroid(clust):
	clust_points = np.array([get_embed(frame) for frame in clust])
	centroid = np.mean(clust_points, axis=0)
	return centroid

def get_error(win, centroid):
	embeds = np.array([get_embed(frame) for frame in win])
	diffs = embeds - centroid
	errors = np.linalg(diffs, ord=2, axis=1)
	return np.mean(errors)

def compute_win_clust_mat(filename_to_clust, window_size=30):
	clust_to_filename = get_clust_to_filename(filename_to_clust)
	video_wins = []
	win_clust_vecs = []
	for clust in clust_to_filename.keys():
		filenames = clust_to_filename[clust]
		centroid = get_centroid(filenames)
		wins = [filenames[i:i+window_size] for i in xrange(len(filenames)-window_size+1)]
		errors = np.array([get_error(win, centroid) for win in wins])
		video_wins.append(wins)
		win_clust_vecs.append(errors)
	win_clust_mat = np.vstack(np.array(win_clust_vecs)) # TODO: check if vstack or hstack
	return (win_clust_mat, video_wins)

def get_best_seqs(projid, window_size=30):	
	# load clustered frames
	with open(os.path.join('static', projid, 'filename_to_clust.pkl'), 'rb') as stream:
		filename_to_clust = pickle.load(stream)

	# contruct matrix for every video
	video_names = filename_to_clust.keys()
	mat_wins = [compute_win_clust_mat(video_clustered_frames, window_size) for video_clustered_frames in filename_to_clust.values()]
	matrices = [mat_win[0] for mat_win in mat_wins]
	wins = [[(win[0], win[-1]) for win in mat_win[1]] for mat_win in mat_wins] # contructs tuples of start and end frames
	flattened_wins = [win for win in vid_wins for vid_wins in wins] 

	# get first indices of videos
	index = 0
	indices = [0]
	for x in xrange(len(wins)):
		index += len(wins[x])
		indices.append(index)

	# concatenate matrices & find best sequences
	mat = np.concatenate(matrices, axis=0)
	argmins = np.argmin(mat, axis=0)
	vid_indices = [bisect.bisect(indices, argmin)-1 for argmin in argmins]
	best_seqs = [(video_names[vid_indices[x]], flattened_wins[argmins[x]]) for x in xrange(len(wins))]
	return best_seqs

if __name__ == "__main__":
	projid = sys.argv[1]
	# window_size
	seqs = get_best_seqs(projid)
	print seqs
