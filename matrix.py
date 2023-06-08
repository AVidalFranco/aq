import os
import math
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import fitter as ft
import pingouin as pg
import statsmodels.api as sm 
plt.style.use("ggplot")


dfBEN = pd.read_csv('Database/BEN_pro.csv', delimiter=';')
dfCO = pd.read_csv('Database/CO_pro.csv', delimiter=';')
dfMXIL = pd.read_csv('Database/MXIL_pro.csv', delimiter=';')
dfNO = pd.read_csv('Database/NO_pro.csv', delimiter=';')
dfNO2 = pd.read_csv('Database/NO2_pro.csv', delimiter=';')
dfO3 = pd.read_csv('Database/O3_pro.csv', delimiter=';')
dfPM25 = pd.read_csv('Database/PM2.5_pro.csv', delimiter=';')
dfSO2 = pd.read_csv('Database/SO2_pro.csv', delimiter=';')
dfTOL = pd.read_csv('Database/TOL_pro.csv', delimiter=';')

# print (dfBEN)

dfBEN.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfCO.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfMXIL.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfNO.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfNO2.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfO3.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfPM25.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfSO2.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]
dfTOL.columns = ["date", "value", "year", "month", "day", "week", "startDate", "endDate", "weekOrder"]


dfBEN = pd.to_numeric(dfBEN["value"], errors="coerce")
dfBEN = dfBEN.iloc[:, 1:5]
print(dfBEN)

# corrBEN = dfBEN.corr()

# print(corrBEN)

# fig, ax = plt.subplots(figsize=(9,9))

# ax = sns.heatmap(
#     corr,
#     vmin=-1, vmax=1, center=0,
#     cmap=sns.diverging_palette(20,220, n=220),
#     square=True
# )


# ax.set_xticklabels(
#     ax.get_xticklabels(),
#     rotation=45,
#     horizontalalignment='right'
# )


# # plt.title("Matriz de correlación do {}".format(columns[0]))
# plt.title("Matriz de correlación das variables")
# plt.show() 