
import os
import numpy as np
import pandas as pd

"""This function acts on the processed database. Its main function
is to select the desired time frames by the user.

Returns:
    - dataMatrix: 2D list with the discrete data ready to be coverted to 
    functional data.
    - timeStamps: the time marks for each time frame."""

def toMatrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def unique(list):
    
    result = []
    
    for i in list:
        if i not in result:
            result.append(i)

    return result

def builder(File, varname, timestep, timeFrame):
    
    fileName, fileExtension = os.path.splitext(File)
    df = pd.read_csv(f'data/{fileName}.csv', delimiter=',') # Set column date as the index?
    cols = list(df.columns.values.tolist())
    
    # Select the data in the specified time frame
    years = list(dict.fromkeys(df['year'].tolist()))
    months = list(dict.fromkeys(df['month'].tolist()))
    months.sort()

    weeks = list(dict.fromkeys(df['week'].tolist()))
    weeks = [i for i in weeks if i != 0]
    weekOrder = list(dict.fromkeys(df['weekOrder'].tolist()))

    startDate = list(df['startDate'])
    endDate = list(df['endDate'])

    days = list(dict.fromkeys(df['day'].tolist()))
    days.sort()
    
    if timestep == '15 min':
        lenMonth = 2976
        lenWeek = 672

    elif timestep == '1 day':
        lenMonth = 31
        lenWeek = 7

    if timeFrame == 'a':

        # Initialize two lists for dataMatrix and timeStamps
        dataMatrix = []
        timeStamps =  []

        # Put the desired data in dataMatrix  and timeStamps
        for i in years:

            df = df.loc[df['year'] == i]

            for j in months:

                df = df.loc[df['month'] == j]

                if df.empty == True:
                    pass
                elif df.empty == False:
                    variable = df[f'{varname}'].values.tolist()

                    if len(variable) == lenMonth:
                        dataMatrix.append(variable)
                        timeStamps.append(f'{j} {i}')
                    else:
                        pass

                df = pd.read_csv(f'data/{fileName}.csv', delimiter=',')

                if j == 12:
                    df = df.loc[df['year'] == (i+1)]
                else:
                    df = df.loc[df['year'] == i]

    elif timeFrame == 'b':

        # Initialize two lists for dataMatrix and timeStamps
        dataMatrix = []
        timeStamps =  []
            
        for i in weeks:
            
            df = df.loc[df['week'] == i]
            
            if df.empty == True:
                pass
            elif df.empty == False:
                variable = df[f'{varname}'].values.tolist()
                
                if len(variable) == lenWeek:
                    dataMatrix.append(variable)
                else:
                    pass
            
            df = pd.read_csv(f'data/{fileName}.csv', delimiter=',')
            
        # Clean startDate and endDate
        startDate = [i for i in startDate if i != '-']
        endDate = [i for i in endDate if i != '-']
        
        for i in zip(startDate, endDate):
            timeStamps.append(str(i))

    elif timeFrame == 'c':
        
        # Initialize two lists for dataMatrix and timeStamps
        dataMatrix = []
        timeStamps =  []
            
        for i in years:
            
            df = df.loc[df['year'] == i]
            
            for j in months:
                
                df = df.loc[df['month'] == j]

                for k in days:
                    
                    df = df.loc[df['day'] == k]
                    
                    if df.empty == True:
                        pass
                    elif df.empty == False:
                        variable = df[f'{varname}'].values.tolist()
                        
                        if len(variable) == 96:
                            dataMatrix.append(variable)
                            timeStamps.append(f'{k} {j} {i}')
                        else:
                            pass

                    df = pd.read_csv(f'data/{fileName}.csv', delimiter=',')
                    
                    if j == 12 and k == 31:
                        df = df.loc[df['year'] == (i+1)]
                        df = df.loc[df['month'] == 1]
                    
                    elif j <= 12:
                        df = df.loc[df['year'] == i]
                        
                        if k < 31:
                            df = df.loc[df['month'] == j]
                        
                        elif k == 31:
                            df = df.loc[df['month'] == (j+1)]

    return dataMatrix, timeStamps

