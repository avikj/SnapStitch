import sys
import os
import time
from extract_frames import main as extract_frames
from get_inception_embeddings import main as get_inception_embeddings
from clustering import get_clusters_for_project
from get_cluster_window_matrix import get_best_seqs
from stitcher import stitch
def main(project_id):
  video_basenames = os.listdir(os.path.join('videos', project_id))
  print 'Videos to process:', video_basenames

  for video_basename in video_basenames:
    print 'Extracting frames from %s.'%video_basename
    extract_frames(project_id, video_basename, sampling_rate=1)
    get_inception_embeddings(project_id, video_basename[:video_basename.index('.')])
  
  video_names = [video_basename[:video_basename.index('.')] for video_basename in video_basenames]
  get_clusters_for_project(project_id, video_names)
  result_seqs = get_best_seqs(project_id, window_size=5)
  print result_seqs
  if not os.path.isdir('results'):
    os.mkdir('results')
  stitch(result_seqs, os.path.join('results', project_id+'.mp4'))
  with open(os.path.join('results', 'finished_'+project_id+'.txt'), 'w') as finished_file:
    finished_file.write('balls')
if __name__ == '__main__':
  result = main(sys.argv[1])
