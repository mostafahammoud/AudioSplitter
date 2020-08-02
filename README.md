# AudioSplitter

This script separates audios files by a desired length. 
It is most usefull in splitting large audiobooks

It also has the option of combining multiple files ahead of time to ensure
they will be split evenly by using combineAudioInDir instead of 
combineAudioByPath

# TO USE:
    - Download the following libraries:
        - pydub
        - math
        - os
        - glob
        - shutil
        - mutagen.mp3
        - librosa
        - subprocess

    - Provide the file names to be be used in paths
    - Provide the direcotry of the output files in savedPath
    - Provode the path of the mergedFile in mergedFilePath
    - Provide te desired lenght of each audio in msec in desiredSegmentLength
    - Provide overlap duiration in overlapDuration

# TO DO:
    - Add the option to automatically detect if a directory or multiple paths have been provided
    - Organize the code to have a section for inputs and section for the code
    - Add the option to call this script from the command prompt
