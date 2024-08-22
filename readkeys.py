"""
Copyright (c) 2024 Seth Egger

Written by Seth W. Egger <sethegger@gmail.com>

Reads google api key from local file, sourceFile

"""

def readkeyfile(sourceFile):
    file = open(sourceFile,'r')

    return file.readlines()