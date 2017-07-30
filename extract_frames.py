import cv2
import argparse
import sys
import datetime
import os
import progressbar
import errno

def main(project_id, video_basename, sampling_rate=3):
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}
    video_name = video_basename[:video_basename.index('.')]
    # extract video frames
    extracted_frame_dir = os.path.join('static', project_id, video_name, 'frames')
    mkdir_p(extracted_frame_dir)
    if not os.path.isdir(extracted_frame_dir):
        os.mkdir(extracted_frame_dir)
    video_path = os.path.join('videos', project_id, video_basename)
    vidcap = cv2.VideoCapture(video_path)
    print('Extracting video frames...')
    bar = progressbar.ProgressBar(maxval=101, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    fps = vidcap.get(cv2.cv.CV_CAP_PROP_FPS)
    success, image = vidcap.read()
    frame_count = 1
    while success:
        success, image = vidcap.read()
        if frame_count % int(round(fps / sampling_rate)) == 0:
            # print('Read a new frame: %f ms'% vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC), success)
            cv2.imwrite(os.path.join(extracted_frame_dir, "%09d.jpg" % vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)), image)
        vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        percent = vidcap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) / int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        bar.update(100 * percent)
        frame_count += 1
    bar.finish()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
if __name__ == '__main__':
    main('videos/vid1.m4v')
