
from os import times
import skfda as fda

from builder import builder
from fda import functionalAnalysis

"""This file performs the univariate functional data analysis
with directional outlyingness"""

# Improvements: in order to not insert the 31s I would have to make several changes
# 1. normalizer.py would need a new version which does the same but does not insert the 31s
# 2. builder.py would need to read the df and load it into a new variable (df_i) in each
# iteration in stead of loading it into the same df variable. This will eliminate the problem
# of the jumping from month to month and day to day. Basically I would not have to use
# the conditionals at the end of every iteration in time frames "a" and "c" to avoid startting
# with an empty df after every iteration.

# Define the data we want to study
varName = 'BEN'
timeStep = "1 day" # 1 day or 15 min
timeFrame = 'b' # 'a' for months, 'b' for weeks, and 'c' for days

preprocessing = 'Y' # Set the preprocessing option

if __name__ == '__main__':
    
    # Continue here: take out amplitude from outDec. Call outDec on the iF, MCD, and kNN methods (if outDec == True, continue, else "No outliers detected")

    # Read the database with the desired time unit and create dataMatrix and timeStamps
    dataMatrix, timeStamps = builder(File=f'data_pro.csv', varname=varName, timestep=timeStep, timeFrame=timeFrame)
    print('[INFO] builder() DONE')
    print(len(dataMatrix), len(timeStamps))

    cutoffIntBox, cutoffMDBBox, cutoffIntMS, cutoffMDBMS = 1.5, 1.5, 0.993, 0.993 # Cutoff params

    # Define depths here
    # integratedDepth = fda.exploratory.depth.IntegratedDepth().multivariate_depth
    modifiedbandDepth = fda.exploratory.depth.ModifiedBandDepth().multivariate_depth
    # projectionDepth = fda.exploratory.depth.multivariate.ProjectionDepth()
    # simplicialDepth = fda.exploratory.depth.multivariate.SimplicialDepth()
    
    outliers = functionalAnalysis(varname=varName, depthname='modified band', datamatrix=dataMatrix, timestamps=timeStamps, 
                                timestep=timeStep, timeframe=timeFrame, depth=modifiedbandDepth, cutoff=cutoffMDBMS, 
                                contamination=0.10, detection_threshold=10)
    print('[INFO] functionalAnalysis() DONE')