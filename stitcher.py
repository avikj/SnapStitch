from moviepy.editor import *

def stitch(data, output):
    clips = []
    for vid in data.keys():
        for seq in data[vid]:
            clips.append(parseClip(vid, seq[0], seq[1]))
    result = concatenate(clips, padding=-1, method="compose")
    result.write_videofile(output, fps=20, bitrate="2500k")


def parseClip(file, start, end):
    return VideoFileClip(file).subclip(start,end).crossfadein(1)


if __name__ == '__main__':
    stitch({
        '1.mp4': [[0, 10], [15, 20]],
        '2.mp4': [[0, 10]],
        '3.mp4': [[0,8], [12,17]],
        '4.mp4': [[12,20]]
    }, 'sex.mp4')
