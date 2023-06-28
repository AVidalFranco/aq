"""Idea for the heatmap:
1. Get the whole list of timeStamps from _full.csv with a for loop such as:
for i in df[weekNumber]):
    access each weak and append the start and end dates
It has to be something similar to the actual timeStamps lists because of the next step.

2. Get (manually <- fix this) the timeStamps of each variable and the timeStamps of the outliers of
each variable. Then compare the three lists that we have now with a another loop:

for i in timeStamps (full):

    if i in timeStamps (outliers) and i in timeStamps (variable):
        append(1)
    
    if i in timeStamps (variable):
        append(0)
    
    if i not in timeStamps (variable):
        append(-1)

Based on the resulting list make those squares who have a value of -1 black to symbolize the abscense of 
data, those with a zero white and those with a 1 blue to mark the outliers in each variable.
"""

import math
import random
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt

# This function gets the weekly timeStamps of a database
def get_timestamps(BEN_pro):
    
    # Read the dataase that contains the starting and ending dates of each week
    df = pd.read_csv(f'Database/{BEN_pro}.csv', delimiter=';')

    timeStamps = []

    startDate = list(df['startDate'])
    endDate = list(df['endDate'])

    # Clean startDate and endDate
    startDate = [i for i in startDate if i != '-']
    endDate = [i for i in endDate if i != '-']

    for i in zip(startDate, endDate):
        timeStamps.append(str(i))
    
    return timeStamps

# This function get the binarized outliers of a certain variable
def binarizer(BEN_pro, timestamps):

    # Get the time stamps present in each variable
    timeStamps_var = get_timestamps(BEN_pro=f'{BEN_pro}')

    # Get the outlying time stamps
    df = pd.read_csv(f'Database/{BEN_pro}.csv', delimiter=';')
    outliers = list(df['timeStamps'])

    binarized_outliers = []
    for i in timestamps:
        if i in outliers:
            binarized_outliers.append(2)
        elif i in timeStamps_var:
            binarized_outliers.append(1)
        else:
            binarized_outliers.append(0)

    return binarized_outliers

# This function converts a list into a square matrix
def list2sqrmatrix(list, option):
    
    closest_sqr = int(np.round(math.sqrt(len(list)), 0))
    
    mat = []
    
    if option == 'binarized':
        param = [0]
    elif option == 'annot':
        param = [np.nan]
    
    while list != []:
        
        if len(list[:closest_sqr]) < closest_sqr:
            mat.append(list[:closest_sqr] + param * (closest_sqr - len(list[:closest_sqr])))
        
        else:
            mat.append(list[:closest_sqr])
        
        list = list[closest_sqr:]
    
    return mat

# This function gets the weekly mean values of a database
def get_meanvalues(filename, list):
    
    df = pd.read_csv(f'Database/{filename}.csv', delimiter=';')
    
    mean_values = []
    for i in (range(1, len(list) + 1)):
        
        mean_values.append(np.round(np.mean(df.loc[df['week'] == i, 'value']), 2))
    
    return mean_values

# This function gets the magnitude and shape values of each function
def get_magshapevalues(filename, var_list):

    # Read the saved files with the magnitude and shape data
    mag = list(np.load(f'Database/{filename}_mag.npy'))
    shape = list(np.load(f'Database/{filename}_shape.npy'))

    # Read the processed database to know which weeks are missing
    df = pd.read_csv(f'Database/{filename}_pro.csv', delimiter=';')

    # Insert a nan in those indices where a week is missing
    for i in (range(1, len(var_list) + 1)):
    
        if (df.loc[df['week'] == i]).empty == True:

            mag.insert(i-1, np.nan)
            shape.insert(i-1, np.nan)
    
    return mag, shape


# Define the file name
fileName = 'Caudal_p'

if __name__ == '__main__':

    # Get all the time stamps. It just needs any normalized variable, I have chose rain in this case
    timeStamps = get_timestamps(filename=f'{fileName}_nor')

    # Get the outlying timeStamps of each variable and binarize them
    binarized_values = binarizer(filename=fileName, timestamps=timeStamps)
    # binarized_pluvio = binarizer(filename='Pluviometria_p_pro', timestamps=timeStamps)

    mat = list2sqrmatrix(list=binarized_values, option='binarized')

    # Get mean values
    mean_values = get_meanvalues(filename=f'{fileName}_pro', list=binarized_values)
    mat_values = list2sqrmatrix(list=mean_values, option='annot')

    # Mean values heatmap
    plt.rcParams['font.size'] = '8'
    fig, ax = plt.subplots(figsize=(7,7))
    ax = sns.heatmap(mat, vmin=0, vmax=2, cmap='Blues', cbar=False, annot=mat_values, annot_kws={"size": 35 / np.sqrt(len(mat))})
    plt.title('Flow heatmap')

    # mag, shape = get_magshapevalues(filename=fileName, var_list=binarized_values)

    # # Turn those values into a square matrix
    # mag_values = list2sqrmatrix(list=mag, option='annot')
    # shape_values = list2sqrmatrix(list=shape, option='annot')

    # # Magnitude heatmap
    # fig, ax = plt.subplots(figsize=(13,13))
    # ax = sns.heatmap(mat, vmin=0, vmax=2, cmap='Blues', cbar=False, annot=mag_values, annot_kws={"size": 35 / np.sqrt(len(mat))})
    # plt.title('Pluviometry heatmap')

    # # Shape heatmap
    # fig, ax = plt.subplots(figsize=(13,13))
    # ax = sns.heatmap(mat, vmin=0, vmax=2, cmap='Blues', cbar=False, annot=shape_values, annot_kws={"size": 35 / np.sqrt(len(mat))})
    # plt.title('Pluviometry heatmap')

    plt.show()

# Heatmap resources
# https://seaborn.pydata.org/generated/seaborn.heatmap.html
# https://pythonbasics.org/seaborn-heatmap/
# https://towardsdatascience.com/5-ways-to-use-a-seaborn-heatmap-python-tutorial-c79950f5add3

