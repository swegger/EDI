"""
Copyright (c) 2024 Seth Egger

Written by Seth W. Egger <sethegger@gmail.com>

"""

import pandas as pd
import re

def readkeyfile(sourceFile):
    '''
    Reads google api key from local file
    '''
    file = open(sourceFile,'r')

    return file.readlines()


def convertGStoPandas(data,headers):
    '''
    Converts google sheet imported by gspread into a pandas data frame
    appropriate for speakerAnalysisProject analysis.
    '''

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


def genSankey(df,cat_cols=[],title='Sankey Diagram',colorScheme='category'):
    '''
    Generates a source-target-count object appropriate for generating
    Sankey plots from a data frame.
    '''
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df.groupby([cat_cols[i],cat_cols[i+1]]).size().reset_index().rename(columns={0:'count'})
            sourceTargetDf.columns = ['source','target','count']
            sourceTargetDf['source'] = cat_cols[i] + '-' +  sourceTargetDf['source'].astype(str)
            sourceTargetDf['target'] = cat_cols[i+1] + '-' +  sourceTargetDf['target'].astype(str)
        else:
            tempDf = df.groupby([cat_cols[i],cat_cols[i+1]]).size().reset_index().rename(columns={0:'count'})
            tempDf.columns = ['source','target','count']
            tempDf['source'] = cat_cols[i] + '-' + tempDf['source'].astype(str)
            tempDf['target'] = cat_cols[i+1] + '-' + tempDf['target'].astype(str)
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # Label list
    temp = sourceTargetDf.groupby(['source','target']).size().reset_index().rename(columns={0:'count'})
    temp = pd.concat([temp['source'],temp['target']])
    labelList = list(dict.fromkeys(temp))

    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    

    # set colors
    colorNumList = []
    if colorScheme == 'category':
        colorPalette = [
        '#636EFA',
        '#EF553B',
        '#00CC96',
        '#AB63FA',
        '#FFA15A',
        '#19D3F3',
        '#FF6692',
        '#B6E880',
        '#FF97FF',
        '#FECB52',
        '#FFE873',
        ]
        for colori in range(len(labelList)):
            if re.search('R1',labelList[colori]):
                colorNumList.append(0)
            elif re.search('R2',labelList[colori]):
                colorNumList.append(5)
            elif re.search('liberal arts',labelList[colori]):
                colorNumList.append(6)
            elif re.search('no research',labelList[colori]):
                colorNumList.append(7)
            elif re.search('international',labelList[colori]):
                colorNumList.append(1)
            elif re.search('\?',labelList[colori]):
                colorNumList.append(2)
            elif re.search('special-focus',labelList[colori]):
                colorNumList.append(3)
            elif re.search('institute',labelList[colori]):
                colorNumList.append(2)
            elif re.search('NIH',labelList[colori]):
                colorNumList.append(4)
            else:
                colorNumList.append(10)
    elif colorScheme == 'Name':
        colorPalette = [
            '#BAB0AC',
            '#9D755D',
            '#FF9DA6',
            '#B279A2',
            '#54A24B',
            '#72B7B2',
            '#E45756',
            '#FFE873',
            ]
        for colori in range(len(labelList)):
            if re.search('Harvard',labelList[colori]):
                colorNumList.append(6)
            elif re.search('UCSF',labelList[colori]):
                colorNumList.append(5)
            elif re.search('Caltech',labelList[colori]):
                colorNumList.append(3)
            elif re.search('Yale',labelList[colori]):
                colorNumList.append(2)
            elif re.search('NYU',labelList[colori]):
                colorNumList.append(4)
            elif re.search('UCSD',labelList[colori]):
                colorNumList.append(1)
            elif re.search('Columbia',labelList[colori]):
                colorNumList.append(0)
            else:
                colorNumList.append(7)
    else:
        for colori in range(len(labelList)):
            colorNumList.append(2)

            
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[colorNum]]


    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig