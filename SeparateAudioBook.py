# -*- coding: utf-8 -*-
"""
Spyder Editor

This script separates audios files by a desired length. 
It is most usefull in splitting large audiobooks

It also has the option of combining multiple files ahead of time to ensure
they will be split evenly by using combineAudioInDir instead of 
combineAudioByPath

TO USE:
    - Provide the file names to be be used in paths
    - Provide the direcotry of the output files in savedPath
    - Provode the path of the mergedFile in mergedFilePath
    - Provide te desired lenght of each audio in msec in desiredSegmentLength
    - Provide overlap duiration in overlapDuration

"""

from pydub import AudioSegment
import math
import os
from glob import iglob
import shutil
from mutagen.mp3 import MP3
import librosa
import subprocess

def main():

    fileName1 = ("C:\\Users\\mhamm\\Documents\\Learning\\Investing\\Books"
                 "\\Rich Dad's Guide To Investing Audio Book Part 1-2.mp3")
    fileName2 = ("C:\\Users\\mhamm\\Documents\\Learning\\Investing\\Books"
                 "\\Rich Dad's Guide To Investing Audio Book Part 2-2.mp3")
    
    paths = [fileName1, fileName2]
    
    savedPath = ("C:\\Users\\mhamm\\Documents\\Learning\\Investing\\Books\\"
                 "RichDadSplit\Rich Dad's Guide To Investing Audio Book")
    
    mergedFilePath = ("C:\\Users\\mhamm\\Documents\\Learning\\Investing"
                      "\\Books\\RichDad's Guide To Investing Audio Book "
                      "Merged.mp3")
    
    # The desired length of the file in seconds
    desiredSegmentLength = 20 * 60
    
    # The desired Overlap between audio segments in seconds
    overlapDuration = 1
    
    combineAudioByPath(paths,mergedFilePath)
    
    # Now that we have approx time, we will create the indicies for the split
    # Need to create a start(in sec) and a duration(in sec)
    
    totalLength = getMp3Length(mergedFilePath)
    
    segmentArray = getSplitArray(totalLength,desiredSegmentLength,
                                 overlapDuration)
    
    cnt = 0
    
    for segment in segmentArray:
        cnt = cnt + 1
        
        # Only Load a part of the Audio needed
        y, sr = loadAudio(mergedFilePath, offset = segment.getLeftIndex(),
                  duration = segment.getDuration())
        
        # Get the path to save the new split Audio
        segment.setPath(savedPath + " Part " + str(cnt) + " - " +
                            str(len(segmentArray)) + '.' + 
                            segment.getFormat())
        
        saveToMp3(y, sr, segment.getPath())
        

# Return Mp3 length in seconds
def getMp3Length(path):
    audio = MP3(path)
    lengthSec = audio.info.length
    
    return lengthSec

# Load the Audio file
# You can only load a part of the file using offset and duration
# Loading a part of the file does not cause the whole file to be read, which 
# will optimise the RAM
def loadAudio(audioPath, offset = 0.0, duration = None):
    y, sr = librosa.load(audioPath,offset=offset,
                              duration=duration)
    return y, sr

# Saves an Audio file to an MP3
def saveToMp3(y, sr, path):
    
    # Save it as a wav file
    # Reason I am saving it as a wav file and not as Mp3 directly is 
    # because, I was unable to find a fucntion in Librosa that can save to 
    # MP3. So I will save to wave then convert to MP3
    librosa.output.write_wav(path, y, sr, norm=False)
    
    # Convert wav to Mp3 using a cmd command
    cmd = 'lame --preset insane %s' % path
    subprocess.call(cmd, shell=True)
    
# Return an array with start, end and duration that will be used to split the 
# audio file later on
def getSplitArray(totalLength,desiredSegmentLength,overlapDuration):
    
    totalLength = math.floor(totalLength)
    
    segmentArray = []
    
    for i in range(0,totalLength,desiredSegmentLength):
        
        leftIndex = i - overlapDuration
        
        if leftIndex < 0:
            leftIndex = 0
        
        rightIndex = i + desiredSegmentLength
        
        if rightIndex > totalLength:
            rightIndex = totalLength
        
        duration = rightIndex - leftIndex
        
        segmentArray.append(Segment(leftIndex,rightIndex,duration = duration,
                                    format = "mp3"))
    
    # It is possible that the last index might not contain the end of the array
    # So we will either add it to the last segment if the size is less than 
    # half the desisredSegmentLength or we will create a new one if it is not
    
    lastRightIndex = segmentArray[-1].getRightIndex()
    
    if lastRightIndex < totalLength:
        
        # If what is left is not too big
        if (totalLength - lastRightIndex) < (desiredSegmentLength/2):
            segmentArray[-1].setRightIndex(totalLength)
            segmentArray[-1].updateDuration
           # If what is left is big
        else:
            segmentArray.append(Segment(lastRightIndex - overlapDuration,
                                  totalLength))
        
    return segmentArray

class Segment:
    def __init__(self, leftIndex, rightIndex, duration = None, path = None, 
                 format = None):
        self.leftIndex = leftIndex
        self.rightIndex = rightIndex
        self.path = path
        self.format = format
        
        if duration == None:
            duration = rightIndex - leftIndex
        
        self.duration = duration
    
    def getLeftIndex(self):
        return self.leftIndex
    def getRightIndex(self):
        return self.rightIndex
    def getDuration(self):
        return self.duration
    def getPath(self):
        return self.path
    def getFormat(self):
        return self.format
            
    def setLeftIndex(self, value):
        self.leftIndex = value
    def setRightIndex(self, value):
        self.rightIndex = value
    def setDuration(self, value):
        self.duration = value
    def setPath(self, path):
        self.path = path
    def setFormat(self, format):
        self.format = format        
        
    def updateDuration(self):
        self.duration = self.rightIndex - self.leftIndex

def combineAudioFiles(paths):
    
    if len(paths) == 0:
        exit("No Path Defined")
        
    # Create a silent audio segment of 1000ms
    audio = AudioSegment.silent(duration=1000) 
    
    for path in paths:
        audio = audio + AudioSegment.from_file(path)
        
    return audio

# This function combines the Audio files by using their paths 
def combineAudioByPath(paths, destPath):
    destination = open(destPath, 'wb')
    for filename in paths:
        shutil.copyfileobj(open(filename, 'rb'), destination)
    #make them all together with for
    destination.close()
    
# This function combines all Audio files of a specific type inside a directory
def combineAudioInDir(directory, audioType, destPath):
    destination = open(destPath, 'wb')
    for filename in iglob(os.path.join(directory, '*.' + audioType)):
        shutil.copyfileobj(open(filename, 'rb'), destination)
    #make them all together with for
    destination.close()
    
if __name__ == "__main__":
    main()
    
