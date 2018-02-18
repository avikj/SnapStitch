import sys, string, os

import subprocess
import random
from collections import defaultdict
import sys

from stitcher import stitch

def videoSummarize():
    name = sys.argv[1]
    print os.path.dirname(name)
    print os.path.basename(name)
    proc = subprocess.Popen(["/usr/local/bin/scenedetect", "-i", name , "-d" , "content" , "-t", "30"], stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
        if line.startswith('00'):
        	sceneClips = ['00:00:00.000'] + line.split(",")
        	print sceneClips



    vidlength = 3
    numberOfFive = (int)(((vidlength*60)/5) / 5)


    for cnt in range(0, ( len(sceneClips) - numberOfFive)) :
      randIdx = random.randint(0, (len(sceneClips) - 1))
      del sceneClips[randIdx]

    sceneClipParts = []  
    clipStartAndEnd = ();

    cnt = 0
    for clipDuration in sceneClips:
        clipDuration =  clipDuration.strip(' \n')
        start = int(clipDuration. split(".")[1])
        parts = (clipDuration. split(".")[0]).split(":")
        start = start + (int(parts[0])) * 3600 * 1000 
        start = start + (int(parts[1])) * 60 * 1000 
        start = start + (int(parts[2])) * 1000
        
        sceneClipParts.insert(cnt, (start, start + 5000))
        cnt = cnt + 1


    print sceneClipParts

    x = {}
    x[name] = sceneClipParts

    output = os.path.splitext(name)[0] + "_output.mp4"
    stitch(x,output)

if __name__ == '__main__':
  videoSummarize()

