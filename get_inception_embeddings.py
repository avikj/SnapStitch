# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Simple image classification with Inception.

Run image classification with Inception trained on ImageNet 2012 Challenge data
set.

This program creates a graph from a saved GraphDef protocol buffer,
and runs inference on an input JPEG image. It outputs human readable
strings of the top 5 predictions along with their probabilities.

Change the --image_file argument to any jpg image to compute a
classification of that image.

Please see the tutorial and website for a detailed description of how
to use this script to perform image recognition.

https://tensorflow.org/tutorials/image_recognition/
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import re
import sys
import tarfile
import pickle
import progressbar
import numpy as np
from six.moves import urllib
import tensorflow as tf

FLAGS = None
MODEL_DIR = '/tmp/imagenet'
# pylint: disable=line-too-long
DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
# pylint: enable=line-too-long

def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      MODEL_DIR, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


def compute_embeddings(images):
  """Runs inference on an image.

  Args:
    image: Image file names.

  Returns:
    Dict mapping image file name to embedding.
  """

  # Creates graph from saved GraphDef.
  create_graph()
  filename_to_emb = {}
  config = tf.ConfigProto(device_count = {'GPU': 0})
  bar = progressbar.ProgressBar(widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
  with tf.Session(config=config) as sess:
    i = 0
    for image in bar(images):
      if not tf.gfile.Exists(image):
        tf.logging.fatal('File does not exist %s', image) 
      image_data = tf.gfile.FastGFile(image, 'rb').read()
      # Some useful tensors:
      # 'softmax:0': A tensor containing the normalized prediction across
      #   1000 labels.
      # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
      #   float description of the image.
      # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
      #   encoding of the image.
      # Runs the softmax tensor by feeding the image_data as input to the graph.
      softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
      embedding_tensor = sess.graph.get_tensor_by_name('pool_3:0')
      embedding = sess.run(embedding_tensor,
                             {'DecodeJpeg/contents:0': image_data})
      filename_to_emb[image] = embedding.reshape(2048)
      i += 1
      # print(image, i, len(images))
  return filename_to_emb

# temp_dir is a subdir of temp 
def main(project_id, video_name):
  '''image = (FLAGS.image_file if FLAGS.image_file else
           os.path.join(MODEL_DIR, 'cropped_panda.jpg'))'''
  temp_dir = os.path.abspath(os.path.join('temp', project_id, video_name))
  # print(temp_dir)
  # print('loading images')
  image_dir = os.path.join(temp_dir, 'frames')
  images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(image_dir) for f in filenames if os.path.splitext(f)[1].lower() in '.jpg.jpeg']
  # print(images)
  print('Computing embeddings for images.')
  filename_to_emb = compute_embeddings(images)
  if not os.path.isdir(os.path.join(temp_dir, 'embeddings')):
    os.mkdir(os.path.join(temp_dir, 'embeddings'))
  for img_filename, emb in filename_to_emb.iteritems():
    emb_filename = img_filename[:-20]+'embeddings'+img_filename[-14:-4]+'.npy'
    np.save(emb_filename, emb)
  pickle_filename = os.path.join(temp_dir, 'filename_to_emb.pkl')
  with open(pickle_filename, 'w') as output_file:
    pickle.dump(filename_to_emb, output_file)
  embs = []
  '''with open('filenames.tsv', 'w') as filenames_file:
    for filename, emb in filename_to_emb.iteritems():
      filenames_file.write(filename+'\n')
      embs.append(emb)
  embs = np.array(embs)
  np.savetxt('embs.tsv', embs, delimiter='\t')'''
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  # classify_image_graph_def.pb:
  #   Binary representation of the GraphDef protocol buffer.
  # imagenet_synset_to_human_label_map.txt:
  #   Map from synset ID to a human readable string.
  # imagenet_2012_challenge_label_map_proto.pbtxt:
  #   Text representation of a protocol buffer mapping a label to synset ID.
  parser.add_argument( # not used, assume default works
      '--model_dir',
      type=str,
      default='/tmp/imagenet',
      help="""\
      Path to classify_image_graph_def.pb,
      imagenet_synset_to_human_label_map.txt, and
      imagenet_2012_challenge_label_map_proto.pbtxt.\
      """
  )
  parser.add_argument(
      '--data_dir',
      type=str,
      help='Directory to recursively find images in and compute embeddings for.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  print (sys.argv[0])
  print (unparsed)
  main(FLAGS.data_dir)
