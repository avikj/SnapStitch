from moviepy.editor import *

def stitch(data, output):
    clips = []
    for vid in data.keys():
        for start, end in data[vid]:
            clips.append(parseClip(vid, start/1000, end/1000).crossfadeout(1))
    clips.append(parseClip('ending.mp4',0,2).resize(clips[0].size))
    result = concatenate(clips, padding=-1, method="compose")
    result.write_videofile(output, fps=20, bitrate="2500k")


def parseClip(file, start, end):
    return VideoFileClip(file).subclip(start,end).crossfadein(1)


if __name__ == '__main__':
    stitch({
        '1.mp4': [[0, 8000], [10000, 4000]],
        '2.mp4': [[0, 5000]]
    }, 'sex.mp4')
