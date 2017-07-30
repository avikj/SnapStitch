import sys
import os
from extract_frames import main as extract_frames
from get_inception_embeddings import main as get_inception_embeddings
from clustering import get_clusters_for_project
def main(project_id):
  video_basenames = os.listdir(os.path.join('videos', project_id))
  print video_basenames 
  for video_basename in video_basenames:
    extract_frames(project_id, video_basename)
    get_inception_embeddings(project_id, video_basename[:video_basename.index('.')])
  video_names = [video_basename[:video_basename.index('.')] for video_basename in video_basenames]
  get_clusters_for_project(project_id, video_names)

if __name__ == '__main__':
  main(sys.argv[1])