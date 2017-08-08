#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
trial_builder.py

For each future subject, exports an .xlsx file containing all experimental conditions,
trial information, and image filenames that will be used during a social 
information playback experiment. The .xlsx files have subject ID code in the
filename so that they can be retrieved just by reporting the participant name in 
social experiment code. 

Created on Fri Aug 04 15:28:43 2017
@author: Olivia Guayasamin
"""
# -----Initializing Steps-----

# import libraries for running experiment
import numpy as np
import scipy as sp
import pandas as pd
import os
import random

# initialize trial list
idList = ["P" + "{:03d}".format(x) for x in range(140)]  # part ID list

# list of partner reliability conditions
relPerf = ['Best', 'Worst', 'Average']
perfList = ["{}".format(a[1]) for x in idList for a in enumerate(relPerf)]

# concatenate and turn turn into data from
tempSet = list(zip(idList, perfList))
idRelTrials = pd.DataFrame(data = tempSet, columns = ['PartID','Reliability'])

# ----- Create list of Media Names -----

# set directory pathname
path = 'C:/Users/SPC0AJV46/Documents/Python Scripts/SocialExp/'
os.chdir(path)  # change path
# create empty list for holding names
mediaDict = {}

# change path
easyDir = os.path.join(path, 'Easy_Stimuli')  # make pathname
os.chdir(easyDir)
# iterate through files in folder 
for i, fileName in enumerate(os.listdir(easyDir)):
    if 'Mask' in fileName:
        pass
    else:                
        tempName = fileName.split("sy")[-1]  # reformat file name
        keyName = tempName.split(".")[0]                           
        mediaDict[keyName] = fileName  # add to list

# ----- Select media for each condition -----

# change directory
trialDir = os.path.join(path, 'Trial_Orders')  # make pathname
os.chdir(trialDir)

# for each participant in list, create trial dataframe using pandas
for i, participant in enumerate(idRelTrials.PartID):
    
    # set up current data frame
    medias = mediaDict.keys()  # copy media list
    fileName = "{}_Design.xlsx".format(participant)  # create output filename
    # identify reliability
    rel = idRelTrials.Reliability[i]
    # create participant dataframe
    colNames = ['PartID', 'Reliability', 'SocCond','SocCondOrder', 
                'DifTreatment', 'Media','MediaFileName', 'MaskFileName', 
                'SocInfoFileName']


    # Select media for the first asocial condition
    asocialDf1 = pd.DataFrame()
    asocial1 = random.sample(medias, 9)  # from list select 9 at random
    [medias.remove('{}'.format(x)) for x in asocial1]  # remove those selected
    # add info to dataframe
    for j, animal in enumerate(asocial1):
        # pick different animal, because in asocial cond the eyetracks need to 
        # from a different animal
        otherAnimal = random.choice([x for x in asocial1 if x is not animal])
        if(j % 2 == 0): # if its an even number
            # create row for data frame
            tempDf = pd.DataFrame([participant, rel, 'Asocial', 1, 'Hard', 
                                  animal, 'Hard{}.png'.format(animal), 
                                  'HardMask{}.png'.format(animal),
                                  'Hard{0}Gaze.xlsx'.format(''.join((otherAnimal, rel)))])
            asocialDf1 = pd.concat([asocialDf1, tempDf.T]) # append row to dataframe
        else:
            tempDf = pd.DataFrame([participant, rel, 'Asocial', 1, 'Easy', 
                                  animal, 'Easy{}.png'.format(animal), 
                                  'EasyMask{}.png'.format(animal),
                                  'Easy{0}Gaze.xlsx'.format(''.join((otherAnimal, rel)))])
            asocialDf1 = pd.concat([asocialDf1, tempDf.T])    
    # randomize this order
    asocialDf1 = asocialDf1.sample(frac=1)
    
    
    # Select media for the social conditions
    socialDf = pd.DataFrame()
    social = random.sample(medias, 18)  # from list select 9 at random
    [medias.remove('{}'.format(x)) for x in social]  # remove those selected
    # add info to dataframe
    for j, animal in enumerate(social):
        if(j % 2 == 0): # if its an even number
            # create row for data frame
            tempDf = pd.DataFrame([participant, rel, 'Social', 1, 'Hard', 
                                  animal, 'Hard{}.png'.format(animal), 
                                  'HardMask{}.png'.format(animal),
                                  'Hard{0}{1}.xlsx'.format(animal, rel)])
            socialDf = pd.concat([socialDf, tempDf.T], ignore_index = True)  # append row to dataframe
        else:
            tempDf = pd.DataFrame([participant, rel, 'Social', 1, 'Easy', 
                                  animal, 'Easy{}.png'.format(animal), 
                                  'EasyMask{}.png'.format(animal),
                                  'Easy{0}{1}.xlsx'.format(animal, rel)])
            socialDf = pd.concat([socialDf, tempDf.T], ignore_index = True)    
            
    # then randomize this order 
    socialDf = socialDf.sample(frac=1)
    socialDf.reset_index(inplace = True, drop = True)
    # put in conditoin order
    socialDf.loc[socialDf.index[0:8], 3] = 1
    socialDf.loc[socialDf.index[9:18], 3] = 2

    
    # Select media for the second asocial condition
    asocialDf2 = pd.DataFrame()  
    asocial2 = random.sample(medias, 9)  # from list select 9 at random
    # add info to dataframe
    for j, animal in enumerate(asocial2):
        # pick different animal, because in asocial cond the eyetracks need to 
        # from a different animal
        otherAnimal = random.choice([x for x in asocial2 if x is not animal])
        # add info to data frame
        if(j % 2 == 0): # if its an even number
            # create row for data frame
            tempDf = pd.DataFrame([participant, rel, 'Asocial', 2, 'Easy', 
                                  animal, 'Easy{}.png'.format(animal), 
                                  'EasyMask{}.png'.format(animal),
                                  'Easy{0}.xlsx'.format(''.join((otherAnimal, rel)))])
            asocialDf2 = pd.concat([asocialDf2, tempDf.T]) 
        else:
            tempDf = pd.DataFrame([participant, rel, 'Asocial', 2, 'Hard', 
                                  animal, 'Hard{}.png'.format(animal), 
                                  'HardMask{}.png'.format(animal),
                                  'Hard{0}.xlsx'.format(''.join((otherAnimal, rel)))])
            asocialDf2 = pd.concat([asocialDf2, tempDf.T])  # append row to dataframe    
    # randomize this order
    asocialDf2 = asocialDf2.sample(frac=1)
    
    
    # put it all together
    partDf = pd.concat([asocialDf1, socialDf, asocialDf2])
    partDf.reset_index(inplace = True, drop = True)
    partDf.columns = colNames
    
    # write and output to an excell file
    writer = pd.ExcelWriter(fileName)
    partDf.to_excel(writer,'Sheet1')
    writer.save()


# i should end up with 120 files, each 36 rows long(not including headers)
