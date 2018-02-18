import cv2
import argparse
import sys
import datetime
import os
import progressbar
import errno
from threading import Thread

CV_CAP_PROP_POS_MSEC = 0 #fucking magic numbers
CV_CAP_PROP_FRAME_COUNT = 7
CV_CAP_PROP_POS_FRAMES = 1
CV_CAP_PROP_FPS = 5

THREAD_COUNT = 4

def extract_frames(video_path, frame_positions, extracted_frame_dir, bar):
    vidcap = cv2.VideoCapture(video_path)
    for frame_pos in frame_positions:
        bar += 1
        vidcap.set(CV_CAP_PROP_POS_FRAMES, frame_pos)
        success, image = vidcap.read()
        # print('Read a new frame: %f ms'% vidcap.get(CV_CAP_PROP_POS_MSEC), success)
        cv2.imwrite(os.path.join(extracted_frame_dir, "%09d.jpg" % vidcap.get(CV_CAP_PROP_POS_MSEC)), image) # TODO (might still work)

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
    fps = vidcap.get(CV_CAP_PROP_FPS)# TODO
    fps = fps if fps != float('nan') else 25
    print 'actual fps', fps, 'sampling rate', sampling_rate
    print('Extracting video frames...')
    extraction_threads = []
    count = [0]
    frames_to_extract = range(0, int(vidcap.get(CV_CAP_PROP_FRAME_COUNT)), int(round(fps / sampling_rate)))
    bar = progressbar.ProgressBar(maxval=len(frames_to_extract)+1, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for frame_positions in chunk(frames_to_extract, THREAD_COUNT):
        thread = Thread(target=extract_frames, args=(video_path, frame_positions, extracted_frame_dir, bar))
        thread.start()
        extraction_threads.append(thread)
    for thread in extraction_threads:
        thread.join()
    bar.finish()

    '''bar = progressbar.ProgressBar(maxval=101, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
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
    bar.finish()'''

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
def chunk(l, n):
    for i in range(n):
        yield l[len(l)*i/n:len(l)*(i+1)/n]
if __name__ == '__main__':
    main('test', '1.mp4')
