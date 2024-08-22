"""
Copyright (c) 2024 Seth Egger

Written by Seth W. Egger <sethegger@gmail.com>

Reads google api key from local file, sourceFile

"""

import pandas as pd

def readkeyfile(sourceFile):
    file = open(sourceFile,'r')

    return file.readlines()


def convertGStoPandas(data,headers):
    df = pd.DataFrame(data, columns=headers)
    cols = df.columns
    for i in range(len(cols)):
        if cols[i] == '':
            df.iloc[0,i] = cols[i-1]+df.iloc[0,i]
        else:
            df.iloc[0,i] = cols[i]+df.iloc[0,i]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    return df