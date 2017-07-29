import cv2
import argparse
import sys
import datetime
import os
import progressbar

def main(video_path, sampling_rate=3):
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # or any {'0', '1', '2'}
    temp_output_dir = './static/temp_' + video_path[video_path.rindex('/')+1:video_path.rindex('.')] + '_' + datetime.datetime.now().strftime('%d%m%y%H%M%S')
    if not os.path.isdir(temp_output_dir):
        os.mkdir(temp_output_dir)
    print temp_output_dir
    # extract video frames
    extracted_frame_dir = os.path.join(temp_output_dir, 'frames')
    if not os.path.isdir(extracted_frame_dir):
        os.mkdir(extracted_frame_dir)
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
            cv2.imwrite(os.path.join(extracted_frame_dir, "%d.jpg" % vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)), image)
        vidcap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
        percent = vidcap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) / int(vidcap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        bar.update(100 * percent)
        frame_count += 1
    bar.finish()


if __name__ == '__main__':
    main('videos/IMG_0409.m4v')