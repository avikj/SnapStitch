import cv2
import argparse
import sys
import datetime
import os
import progressbar
import errno

CV_CAP_PROP_POS_MSEC = 0 #fucking magic numbers
CV_CAP_PROP_FRAME_COUNT = 7
CV_CAP_PROP_POS_FRAMES = 1
CV_CAP_PROP_FPS = 5

def main(project_id, video_basename, sampling_rate=3):
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}
    video_name = video_basename[:video_basename.index('.')]
    # extract video frames
    extracted_frame_dir = os.path.join('temp', project_id, video_name, 'frames')
    mkdir_p(extracted_frame_dir)
    if not os.path.isdir(extracted_frame_dir):
        os.mkdir(extracted_frame_dir)
    video_path = os.path.join('videos', project_id, video_basename)
    vidcap = cv2.VideoCapture(video_path)
    print('Extracting video frames...')
    bar = progressbar.ProgressBar(maxval=101, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    fps = vidcap.get(CV_CAP_PROP_FPS)# TODO
    fps = fps if fps != float('nan') else 25
    print 'actual fps', fps, 'sampling rate', sampling_rate
    success, image = vidcap.read()
    frames_to_extract = range(0, int(vidcap.get(CV_CAP_PROP_FRAME_COUNT)), int(round(fps / sampling_rate)))
    frame_count = len(frames_to_extract)
    for frame_pos in bar(frames_to_extract):
        vidcap.set(CV_CAP_PROP_POS_FRAMES, frame_pos)
        success, image = vidcap.read()
        # print('Read a new frame: %f ms'% vidcap.get(CV_CAP_PROP_POS_MSEC), success)
        cv2.imwrite(os.path.join(extracted_frame_dir, "%09d.jpg" % vidcap.get(CV_CAP_PROP_POS_MSEC)), image) # TODO (might still work)

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
    main('test', '1.mp4')
